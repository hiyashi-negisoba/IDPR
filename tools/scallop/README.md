# Scallop runtime

The fraud RuleIR runtime tests use the official native `scli` executable instead of
`scallopy`. Scallop 0.2.4 does not publish a Python 3.11/3.12 Linux wheel, while this
project requires Python 3.11 or newer.

Install the pinned runtime:

```bash
scripts/install_scallop_runtime.sh
```

- Version: `0.2.4`
- Asset: `scli-0.2.4-linux-x86_64`
- SHA-256: `8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a`

The downloaded executable is ignored by Git. Only the installer, checksum, generated
Scallop source, and test reports are tracked.
