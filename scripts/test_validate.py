"""Sleep-inclusive timer regressions; uses only fake clocks and processes.

Run beside validate.py with `python -m unittest test_validate.py`. For an isolated
candidate, set QEC360_VALIDATOR_UNDER_TEST to that validator's source path.
"""
import ast
from contextlib import redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

SOURCE = Path(os.environ.get(
    'QEC360_VALIDATOR_UNDER_TEST', Path(__file__).with_name('validate.py')))
SPEC = importlib.util.spec_from_file_location('validator_under_test', SOURCE)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class Clock:
    def __init__(self, value=0.0):
        self.value = value

    def now(self):
        return self.value


class Process:
    """Advance a fake clock when a process wait completes or is interrupted."""
    args = ['synthetic-check']
    pid = 123

    def __init__(self, clock, advance=0.1, completes=True, done=False):
        self.clock, self.advance, self.completes = clock, advance, completes
        self.returncode = 0 if done else None
        self.waits = []

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.waits.append(timeout)
        self.clock.value += self.advance
        if self.completes:
            self.returncode = 0
            return 0
        raise subprocess.TimeoutExpired(self.args, timeout)


class ClockSelectionTests(unittest.TestCase):
    def test_supported_platforms_choose_sleep_inclusive_clock(self):
        for platform, constant in [('Darwin', 'CLOCK_MONOTONIC_RAW'),
                                   ('Linux', 'CLOCK_BOOTTIME')]:
            with self.subTest(platform=platform):
                clock_gettime = Mock(return_value=123.5)
                fake_time = SimpleNamespace(clock_gettime=clock_gettime, **{constant: 42})
                with patch.object(validator.platform, 'system', return_value=platform), \
                        patch.object(validator, 'time', fake_time):
                    now, name = validator.sleep_inclusive_clock()
                    self.assertEqual(name, constant)
                    self.assertEqual(now(), 123.5)
                    clock_gettime.assert_called_once_with(42)

    def test_missing_supported_clock_fails_closed(self):
        for platform in ['Darwin', 'Linux']:
            with self.subTest(platform=platform), \
                    patch.object(validator.platform, 'system', return_value=platform), \
                    patch.object(validator, 'time', SimpleNamespace()):
                with self.assertRaises(RuntimeError):
                    validator.sleep_inclusive_clock()

    def test_unsupported_platform_fails_closed(self):
        with patch.object(validator.platform, 'system', return_value='Unsupported'):
            with self.assertRaises(RuntimeError):
                validator.sleep_inclusive_clock()


class DeadlineTests(unittest.TestCase):
    def test_process_completes_before_deadline(self):
        clock = Clock()
        process = Process(clock)
        validator.wait_until_deadline(process, 900, clock.now)
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.waits, [0.25])

    def test_already_finished_process_does_not_wait(self):
        clock = Clock()
        process = Process(clock, done=True)
        validator.wait_until_deadline(process, 900, clock.now)
        self.assertEqual(process.waits, [])

    def test_already_expired_deadline_does_not_wait(self):
        for now in [900, 901]:
            with self.subTest(now=now):
                clock = Clock(now)
                process = Process(clock)
                with self.assertRaises(subprocess.TimeoutExpired):
                    validator.wait_until_deadline(process, 900, clock.now)
                self.assertEqual(process.waits, [])

    def test_suspend_consumes_deadline_after_one_short_wait(self):
        clock = Clock()
        process = Process(clock, advance=1000, completes=False)
        with self.assertRaises(subprocess.TimeoutExpired):
            validator.wait_until_deadline(process, 900, clock.now)
        self.assertEqual(process.waits, [0.25])

    def test_short_remaining_interval_caps_the_wait(self):
        clock = Clock(899.9)
        process = Process(clock, advance=0.01)
        validator.wait_until_deadline(process, 900, clock.now)
        self.assertAlmostEqual(process.waits[0], 0.1)

    def test_successful_exit_after_deadline_is_rejected_by_stage_guard(self):
        # Exercise the actual nested stage runner without constructing a Lake
        # project or invoking subprocesses; its body is extracted unchanged.
        module = ast.parse(SOURCE.read_text())
        main = next(node for node in module.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'main')
        run = next(node for node in main.body
                   if isinstance(node, ast.FunctionDef) and node.name == 'run')
        clock = Clock()
        process = Process(clock, advance=1000)
        report = {'steps': []}
        with tempfile.TemporaryDirectory() as directory:
            namespace = dict(output=Path(directory), project=Path(directory), env={},
                             elapsed_now=clock.now, report=report, save=Mock(),
                             wait_until_deadline=validator.wait_until_deadline,
                             subprocess=SimpleNamespace(Popen=Mock(return_value=process),
                                                        STDOUT=subprocess.STDOUT,
                                                        TimeoutExpired=subprocess.TimeoutExpired),
                             os=SimpleNamespace(killpg=Mock()), signal=validator.signal)
            exec(compile(ast.Module(body=[run], type_ignores=[]), str(SOURCE), 'exec'), namespace)
            with redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
                namespace['run']('synthetic-check', process.args, 900)
            self.assertEqual(report['steps'][0]['exit_code'], 0)
            self.assertTrue(report['steps'][0]['timeout'])
            self.assertEqual(report['steps'][0]['seconds'], 1000)
            namespace['os'].killpg.assert_not_called()


class StandaloneIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.project = Path(self.directory.name)
        self.output = self.project / 'replay'
        self.output.mkdir()
        self.package = self.project / 'scripts'
        self.package.mkdir(parents=True)
        self.local = self.project / 'BBDistance/Example.lean'
        self.baseline = self.project / '.lake/packages/QEC/QEC/Example.lean'
        for path in (self.local, self.baseline):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('-- fixture\n')
        self.report = {
            'source_sha256': {'BBDistance.Example': validator.digest(self.local)},
            'baseline_source_sha256': {'QEC.Example': validator.digest(self.baseline)},
        }
        for path, key in (
            (self.project / 'lean-toolchain', 'lean_toolchain_sha256'),
            (self.project / 'lake-manifest.json', 'lake_manifest_sha256'),
            (self.project / 'lakefile.toml', 'lakefile_sha256'),
            (self.project / 'provenance/module-migration.json', 'migration_map_sha256'),
            (self.package / 'KernelReplay.lean', 'checker_source_sha256'),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture')
            self.report[key] = validator.digest(path)
        self.report['compiled_sha256'] = {}
        self.report['replay_support_sha256'] = {}
        for relative in ('BBDistance.olean', 'BBDistance/Example.olean.private',
                         'QEC/Example.olean'):
            path = self.output / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'fixture')
            self.report['compiled_sha256'][relative] = validator.digest(path)

    def verify(self):
        validator.verify_unchanged_inputs(self.project, self.output, self.package,
                                         self.report, replay_artifacts=True)

    def test_dependency_and_local_sources_are_resolved_separately(self):
        self.verify()
        self.baseline.write_text('-- changed dependency\n')
        with self.assertRaisesRegex(RuntimeError, 'changed or disappeared'):
            self.verify()

    def test_changed_local_source_is_rejected(self):
        self.local.write_text('-- changed proof\n')
        with self.assertRaisesRegex(RuntimeError, 'changed or disappeared'):
            self.verify()

    def test_root_and_nested_replay_artifacts_are_both_bound(self):
        for relative in ('BBDistance.olean', 'BBDistance/Example.olean.private',
                         'QEC/Example.olean'):
            with self.subTest(relative=relative):
                path = self.output / relative
                path.write_bytes(b'changed')
                with self.assertRaisesRegex(RuntimeError, 'changed or disappeared'):
                    self.verify()
                path.write_bytes(b'fixture')

    def test_extra_replay_artifact_is_rejected(self):
        (self.output / 'BBDistance/Extra.olean').write_bytes(b'extra')
        with self.assertRaisesRegex(RuntimeError, 'inventory changed'):
            self.verify()


if __name__ == '__main__':
    unittest.main()
