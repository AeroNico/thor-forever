# Setup assistant prototype

`Check-Setup.cmd` is a read-only preflight. The final package's
`Install-Thor-Forever.cmd` calls a separate installer; source-only downloads do
not contain its binary dependencies. See `START-HERE.md` before any test.

A separate developer-only `install-components.sh` is now present. It is not
invoked by Check-Setup.cmd and requires a vetted `payload/` which is deliberately
absent from this source draft. The second private Android attempt completed,
and subsequent gameplay, settings persistence and direct-entry tests passed.
Do not run it as a finished public installer.

For a future device test, extract the complete package as `Download/Thor-Forever`, open the GameHub container desktop and run `installer/Check-Setup.cmd`. Read `installer/setup-check.txt`. No terminal commands or path editing should be needed for a standard supported installation.

Supported discovery: GameHub Lite Ludashi, Forever Beta's `WowB-ARM64.exe`, under either standard Program Files directory in a virtual container. The assistant rejects an ambiguous match instead of guessing. Custom-folder selection and a graphical results screen remain unimplemented. The private integrated installer passed on Android. The final package uses `release-v1` under the dedicated Thor Forever root; private attempts are not overwritten. Switching back to the old startup entry is documented, but automatic cleanup is not implemented.

`stage-game.sh` is an internal library called by the developer-only component installer. It
prepares separate executable files and settings under a new `game/` directory,
verifies copies and refuses an existing destination. It does not copy account
settings, caches or logs. Large CASC Data remains shared through a link, **not a
read-only mount**; never run Battle.net or an updater against the staged layout.
This library ran successfully as part of the second private Android attempt.

The developer installer now stops after preparing components and the separate
game layout. It does not launch WoW, change GameHub's startup entry or declare
the installation playable. Once the dedicated attempt directory exists,
`result.txt` records the last phase and exit code in English. A zero exit is
reported as `PREPARED_NOT_VALIDATED`, never as a completed acceptance test.
Detailed `install.log` output is private and may contain local paths. Early
preflight failures occur before that report directory exists.

The checker does not inspect executable contents, so a match is not proof of the correct client version or architecture. File presence is only the first preflight stage.

Private reports must not be uploaded automatically. There is no telemetry or network request in this checker.
