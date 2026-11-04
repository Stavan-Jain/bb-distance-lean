#!/usr/bin/env python3
"""Check import coverage, the pinned dependency, and the extraction boundary."""
from pathlib import Path
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = tomllib.loads((ROOT / 'lakefile.toml').read_text())
    qec = next(p for p in config['require'] if p['name'] == 'QEC')
    assert re.fullmatch(r'[0-9a-f]{40}', qec['rev']), 'QECLean must use a full commit SHA'
    manifest = json.loads((ROOT / 'lake-manifest.json').read_text())
    locked = next(p for p in manifest['packages'] if p['name'] == 'QEC')
    assert locked['rev'] == locked['inputRev'] == qec['rev'], 'QECLean pin and lock disagree'
    assert locked['url'] == qec['git'], 'QECLean URLs disagree'
    migration = json.loads((ROOT / 'provenance/module-migration.json').read_text())
    local = {p.relative_to(ROOT).with_suffix('').as_posix().replace('/', '.'): p
             for p in (ROOT / 'BBDistance').rglob('*.lean')}
    local['BBDistance'] = ROOT / 'BBDistance.lean'
    visiting, seen = set(), set()

    def visit(module):
        assert module in local, f'Missing local module: {module}'
        assert module not in visiting, f'Import cycle: {module}'
        if module in seen:
            return
        visiting.add(module)
        text = local[module].read_text()
        for row in re.findall(r'^import (.+)$', text, re.M):
            for dependency in row.split():
                assert dependency not in migration['modules'], f'Stale import: {dependency}'
                if dependency == 'BBDistance' or dependency.startswith('BBDistance.'):
                    visit(dependency)
        visiting.remove(module)
        seen.add(module)

    visit('BBDistance')
    assert seen == set(local), f'Unreachable modules: {sorted(set(local) - seen)}'
    assert set(migration['modules'].values()) <= seen, 'Extraction omitted source modules'
    assert not (ROOT / 'QEC').exists(), 'QECLean sources must remain a dependency'
    print(f'Layout OK: {len(local)} local modules; QECLean pinned to {qec["rev"]}.')


if __name__ == '__main__':
    main()
