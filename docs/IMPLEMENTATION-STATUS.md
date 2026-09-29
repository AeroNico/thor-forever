# Implementation status

Project name: **Thor Forever**. The owner's working installation is not a development test target and has not been changed by this packaging work.

Implemented:

- English documentation and public-post draft.
- Read-only discovery with no personal container identifiers.
- Explicit missing/multiple-installation handling.
- Standard-location support with spaces and safe quoting.
- Source-only publication allowlist and basic private-path checks.
- Temporary-fixture discovery tests.

Validation: six host-shell tests passed (missing installation, two standard
directory layouts, ambiguous installations, empty executable, and a container
name containing spaces/shell metacharacters). The publication gate passed for
the current source-only tree. These are not Android end-to-end installation tests.

A separate private development probe is prepared to test clean Wine prefix
creation using the already-installed runtime. It does not copy a personal prefix
or launch the game. Its result is pending and it is not a public installer.

First device probe: Wine exited before initialization because the empty prefix
directory did not exist. This runtime requires that directory to be created
explicitly. A second isolated probe creates it first; its outcome is pending.
The first result does not establish that clean initialization is unsupported.

Second device probe: wineboot returned zero and registry files appeared, but
`cryptbase.SystemFunction036` forwarding failed and the Windows-visible
`ntdll.dll` and `cryptbase.dll` were absent. Exit status alone is not sufficient
validation. Third probe seeds matching runtime DLLs into a new empty prefix
before initialization; no personal prefix is copied. Result pending.

Third probe: seeded DLLs remained present and ntdll matched the runtime, but
cryptbase forwarding still failed during initialization. Do not treat this as a
successful clean prefix. Fourth probe explicitly creates and verifies C:/Z:
drive links before initialization, following the previously prepared prefix's
mapping scheme. This tests a path-resolution hypothesis; result pending.

Fourth probe: C:/Z: mappings verified, ntdll matched, and the cryptbase forwarding
failure no longer appeared. Wine displayed a Mono installer prompt; initialization
hit the 90-second timeout (exit 124). Registry/DLL presence is not enough to call
this a successful unattended bootstrap. Fifth probe disables mscoree/mshtml only
in the test process environment to avoid optional installer prompts. Pending.

Fifth device probe PASSED the bootstrap checks: wineboot exit 0, server wait
exit 0, both registry files present, both required system32 DLLs present and
ntdll identical to the selected runtime. No personal prefix was copied.
Other Wine setup/driver warnings remain in the private log. This is not yet a
gameplay or a complete end-to-end installer test.

The same sequence is now extracted into installer/create-prefix.sh, with a
restricted dedicated destination, existing-target refusal, symlink-ancestor
checks and subshell-scoped environment. The extracted function has syntax
validation only; the successful device test used the development probe05.

Graphics probe02 passed in the fresh probe05 prefix: user observed the window
open and close, DXVK 2.4.1 logged device/swapchain creation and presentation,
and the process and script returned zero. The first graphics probe stopped
before execution; the second preserves existing test-prefix DLLs before
installing DXVK. This validates a basic D3D11 clear/present test, not the
game's shader workload or in-world behavior in the new prefix.

Clean-prefix WoW test01 reached in-world gameplay, confirmed by the owner.
Test uses a separate executable directory, separate WTF/cache/log directories
and shared CASC Data, not a copied personal prefix. The owner reported a new
visual regression: rectangular gaps/artifacts in the All Objectives tracker
header when opening a menu, absent in their established setup. Root cause is
not established. Visible DXVK configuration values match the earlier recorded
working run. Do not claim visual parity or a fully validated public installer.

Follow-up: the working graphics settings differed materially from the fresh
profile. Copying the allowlisted graphics keys into the test profile (with a
backup, keeping account/UI settings separate) removed the menu-only artifacts
according to the owner. This establishes that the combined graphics change
resolved the symptom in this test; it does not identify a single responsible
setting. The English starter profile now records those graphics values and the
earlier bootstrap/gameplay flags; the assembled public profile still needs an
end-to-end installer test.

The reusable private test launcher initially contained a generation bug (`$`
instead of `$$` in its process-identity checks). Correcting those three sites
restored launch; this was not a Wine or GameHub regression.

Not implemented/validated:

- Custom-directory picker and graphical wizard.
- Fully specified third-party source/build manifest and binary licensing package.
- Validation of the extracted generic initializer (private clean-prefix and
  gameplay probes have passed without copying a personal prefix).
- Transactional component installation and upgrade/rollback.
- Portable production launcher with error reporting and verified lifecycle behavior.
- End-to-end fresh installation on Android.

The prototype intentionally stops rather than installing an incomplete or unverified runtime. Do not advertise it as a ready-to-use installer.

Component installer development: installer/install-components.sh now verifies
seven pinned input hashes, requires free internal storage, refuses an existing
destination, extracts only the pinned runtime into a dedicated directory,
initializes an isolated prefix and installs DXVK while preserving its initial
builtin DLLs. It does not change the GameHub startup entry or start WoW.
Missing payloads fail closed. Incomplete installations are retained for diagnosis,
not automatically deleted or retried over existing files.

Host validation: the exact runtime tar passed an archive-member audit (2,591
entries, 929,338,440 unpacked bytes). Tests reject traversal, escaping links,
special files, duplicate entries and files nested beneath links. Shell syntax
and the source publication allowlist passed. The generalized component installer
has NOT been executed on Android; its device validation is still pending.

Game staging development: `installer/stage-game.sh` extracts the private
probe's layout preparation into a reusable internal library. It verifies copied
executable-side files, seeds separate settings, rejects existing destinations
and does not copy personal account settings. CASC Data remains shared and is
not read-only. No launcher/updater is invoked. This step is not wired into the
component installer at that stage of development, and was not deployed to the device.

Host staging tests: existing-target refusal and missing-Data refusal passed.
The two successful-layout tests are explicitly skipped on this Windows host
because directory symlink creation was denied; they are NOT recorded as passed.
The failed link operation did not create a game-ready marker or alter original
settings. Full layout checks still require a symlink-capable host or Android.

Integration follow-up: the developer component installer now calls game staging
after verified DXVK copies. All four other copied component binaries also receive
byte-for-byte verification. It writes an English phase/exit report on completion
or failure after creating its dedicated attempt directory. Successful preparation
is explicitly `PREPARED_NOT_VALIDATED`; no launch or startup-entry change occurs.
Nine report scenarios passed host tests (eight stopped phases and preparation).
Shell syntax and the source-only publication gate passed. The integrated flow
still has not run on Android; the two symlink-dependent layout tests remain skipped.

First integrated Android attempt stopped during payload verification (exit 9),
before runtime extraction. Read-only inspection showed that GameHub prepended
two diagnostic messages without newlines to an otherwise correct SHA-256 line.
The parser now strips only the three explicitly recognized wrapper diagnostics
and still requires the exact full digest and filename. Ten host parser cases
passed, including wrong digests, wrong filenames and unrecognized noise rejection.
A second private attempt targets `install-v2`, preserving the failed `install-v1`
and its reports. Its Android outcome is pending; this is not release approval.

Second integrated attempt completed on Android with installer exit 0 and
`STATUS=PREPARED_NOT_VALIDATED`. All seven pinned payloads passed verification,
the separate runtime/prefix initialized, component copy checks passed, and the
separate game layout was prepared under `install-v2`. Wine emitted setup/driver
warnings; exit zero does not prove gameplay. A private launcher now targets only
this new runtime, driver, prefix and starter profile, with a shared launch lock
and per-run logs. Its gameplay and settings-persistence checks are pending.

Owner acceptance follow-up: the install-v2 game reached login and gameplay.
Gamepad settings changed during that test remained enabled after exiting and
relaunching. This confirms observed gameplay and settings persistence for this
installation on the owner's device. A new direct Windows entry wrapper is being
tested separately; cold-start GameHub entry and a second device remain unverified.

Direct-entry follow-up: the owner confirmed both the new Windows test executable
from the desktop and direct launch after selecting it as GameHub's Startup File
Path. The gameplay installation was not replaced; the startup selection was
changed for this test. Full reboot, interruption recovery and a final public
launcher/package are still pending. See VALIDATION.md for the current acceptance
record and RECOVERY.md before switching entries or considering cleanup.

The owner subsequently confirmed direct launch after a full console reboot.
Private installation acceptance now includes fresh-prefix setup, gameplay,
settings persistence, direct GameHub entry and reboot. Public packaging is still
separate work: Wine's complete commit was verified from the public repository,
upstream Wine/DXVK notices and the DXVK compiler patch were collected, and the
original assertion-tracer source was included. SOURCE-PROVENANCE.md records
remaining binary-distribution and reproducible-build gaps. No repository has
been created or pushed and no binary kit is approved for public distribution.

Publication follow-up: the owner approved the public repository
https://github.com/AeroNico/thor-forever and credited u/BryTheGuy06. Reviewed
source and documentation are now pushed there; no binary release was uploaded.
The final-name Windows ARM64 launcher compiled with warnings treated as errors,
and private candidate packaging verified the seven component hashes. Static
tests check final paths, bridge targets and settings names. The final candidate
uses Download/Thor-Forever and a separate release-v1 destination; it does not
overwrite private install-v1/install-v2 attempts. Its device acceptance remains
pending because the AYN Thor is currently disconnected from ADB. Two host
directory-symlink tests remain explicitly skipped on Windows, not counted as
passed. The owner-confirmed earlier Android layout test remains recorded above.

Final-folder acceptance completed: setup-report recorded installer exit 0 under
Download/Thor-Forever using release-v1. The owner confirmed excellent gameplay,
then direct GameHub launch after restart and persisted gamepad controls. The
initial absence of a report was traced to the user not yet pressing the first
CMD confirmation key; installation ran successfully after that prompt. No
runtime change was needed. Functional acceptance of this candidate is complete
on this device; third-party source/notice packaging remains separate.
