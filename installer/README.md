# Installer internals

Players should open the root `Install-Thor-Forever.cmd` and follow START-HERE.md.
Do not launch individual shell scripts manually. GitHub source-only downloads
do not contain the seven required binary payloads.

`Check-Setup.cmd` is an optional read-only preflight. It discovers a single
standard Forever Beta ARM64 installation in GameHub Lite Ludashi. Missing or
ambiguous game paths stop the process. Custom-folder selection is not provided.

The root installer calls `setup.sh`, then `install-components.sh`, which checks
pinned hashes, free space, destination safety and component copies. It creates
a new prefix and stages executable-side game files and fresh settings. It never
imports a personal prefix or account configuration. Existing destinations are
refused, including unfinished attempts. This is not an upgrade/repair command.

Large CASC Data is shared through a link, **not a read-only mount**. Never point
Battle.net or an updater at the separate game layout. GameHub's original runtime
and game installation are not replaced. Direct entry is selected manually.

The installation report uses `PREPARED_NOT_VALIDATED` after successful setup:
preparation is not proof that a game session works on a new device. Confirm
gameplay and settings persistence separately. The final-folder procedure passed
on the owner's Thor; see docs/VALIDATION.md for evidence and limits.

Reports and launch logs stay local and may contain paths or account-related
diagnostics. Review/redact them before sharing. There is no telemetry or
automatic upload. The `--test-attempt-02` option in the internal component
installer is historical developer support, not a user installation instruction.
