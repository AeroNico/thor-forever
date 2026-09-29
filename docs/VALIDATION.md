# Validation record

## Scope

These results apply to one owner's AYN Thor with Adreno 740 and GameHub Lite
Ludashi. They are manual acceptance observations, not benchmarks or a guarantee
for other hardware, accounts, game builds or GameHub variants.

The test used a newly initialized Wine prefix, separately installed runtime,
driver and graphics libraries, and separate executable-side game files. It did
not copy a personal Wine prefix, account directory or saved settings. Large
CASC Data remains shared with the existing game installation through a link;
this is **not a read-only mount**. The installer does not run Battle.net.

## Confirmed on the device

| Check | Evidence / result |
| --- | --- |
| Input component integrity | All seven pinned payload hashes accepted in the second integrated attempt. |
| Separate installation | Installer exited 0 after prefix initialization, verified component copies and game staging. |
| Launch through test script | Owner reached login and reported working gameplay. |
| Settings persistence | Gamepad controls selected in one run remained enabled after a subsequent launch. |
| Windows launcher | Owner opened the new test EXE from the container desktop and confirmed game launch. |
| Direct GameHub entry | Owner selected the test EXE as Startup File Path and confirmed direct launch from GameHub. |
| Full device restart | Owner restarted the console and confirmed direct GameHub launch still worked. |

The original gameplay installation was not overwritten. Direct-entry testing
does change the selected container's startup path; that selection can be
reverted to the previously recorded path without deleting either installation.

## Resolved test failures

- The first integrated installer stopped before extraction. GameHub prepended
  diagnostic text to the correct SHA-256 output without line breaks. The parser
  now strips only the observed diagnostic prefixes, then checks the full hash
  and filename. The checksum requirement was not disabled.
- An earlier fresh-profile test showed gaps in the objectives header while a
  menu was open. Matching the known-working graphics settings removed that
  symptom according to the owner. No single responsible setting was identified.

## Still unverified

- The final downloadable package and beginner instructions on another device.
- Repeated-launch rejection and interrupted-launch recovery in the new entry.
- Game updates: copied executable-side files may become stale relative to the
  shared Data. The private launcher checks the main executable against the
  original and stops if it differs; there is no packaged update workflow yet.
- Remembered account name in the newly installed test environment. This worked
  in the older installation but was not separately reconfirmed in this test.
- A cleanup/uninstall procedure that preserves user-created settings and Data.
- Publication-ready source, license and build provenance for every binary.

Do not report a component-install exit code as proof of gameplay. Both the
installer output and the owner's subsequent acceptance observations are needed.
