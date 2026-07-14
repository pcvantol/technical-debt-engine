# CLI reference

Global options: `--help`, `--version`, `--verbose`, `--quiet`, `--config PATH`, `--output PATH`, `--format {human,json}`, and `--log-level {ERROR,WARNING,INFO,DEBUG,TRACE}`.

The CLI validates arguments, loads configuration, invokes only the public Runtime API, renders console/JSON output, and maps generic outcomes to canonical exit codes. It does not implement capability logic, invoke analyzers, normalize measurements, qualify findings, or generate reports independently.

See [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md), [EXIT_CODES.md](EXIT_CODES.md), and [LOGGING.md](LOGGING.md).
