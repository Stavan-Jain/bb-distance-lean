# Gross certificate generators

Run from the repository root, using Python's standard library:

```sh
python3 scripts/gross/generate.py --verify
python3 scripts/gross/generate.py --force
```

`--verify` compares freshly emitted files without modifying the repository.
`--force` regenerates both data modules. Without either flag, existing outputs
are protected from overwriting.

| Generator | Input | Output |
|---|---|---|
| `gen_bz.py` | The code polynomials and fixed kernel basis in the script | `BBDistance/Gross/SeamBZData.lean` |
| `gen_packaging.py` | `data.json` | `BBDistance/Gross/StabilizerCodeData.lean` |

The first generator validates the peeling order, information sets, 252 light
boundaries, and both Brouwer–Zimmermann walks before emitting data. The second
emits the candidate rank, decoder, and logical-basis certificates. Lean checks
every certificate used by the formal proof; these scripts are outside the
trusted proof base. Change the generator or its input, then regenerate; do not
edit generated Lean files directly.

These generators were imported from qec-lab commit
`aca715a4d03ecc6438b6300105b4f8446c318abe`, with paths and command-line handling
adapted to this repository. The mathematical data and emission algorithms are
preserved.

For independent kernel replay of both case studies, use the shared validator:

```sh
python3 scripts/validate.py --output /path/to/new-validation-directory --profile
```

It first rebuilds every local Lean module from source, then replays all safe
declarations against the pinned QECLean imports. See the
[validation details](../bravyi360/README.md#validation).
