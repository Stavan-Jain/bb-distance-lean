#!/usr/bin/env python3
"""Reproduce the Gross data modules without running a Lean build."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--verify', action='store_true', help='compare without overwriting')
    mode.add_argument('--force', action='store_true', help='overwrite generated modules')
    args = parser.parse_args()
    modules = [('gen_bz.py', 'SeamBZData.lean', ['--emit']),
               ('gen_packaging.py', 'StabilizerCodeData.lean', [])]
    with tempfile.TemporaryDirectory(prefix='gross-certificates-') as directory:
        generated = []
        for emitter, name, flags in modules:
            staged = Path(directory) / name
            subprocess.run([sys.executable, str(PACKAGE / emitter), *flags,
                            '--out', str(staged)], check=True)
            target = REPO / 'BBDistance/Gross' / name
            if args.verify:
                if not target.is_file() or target.read_bytes() != staged.read_bytes():
                    raise SystemExit(f'Reproduction mismatch: {target}')
            elif target.exists() and not args.force:
                raise SystemExit(f'Refusing to overwrite {target}; pass --force.')
            generated.append((staged, target))
        if not args.verify:
            for staged, target in generated:
                target.write_bytes(staged.read_bytes())
    print(('Verified' if args.verify else 'Generated') + ' both Gross data modules.')


if __name__ == '__main__':
    main()
