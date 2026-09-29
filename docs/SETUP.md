# Setup design and acceptance tests

Developer background for the experimental installer. Players should follow
START-HERE.md. The generalized procedure passed in an isolated environment on
the owner's device; independent-device validation is still outstanding.

## 1. Preserve the existing setup

Record GameHub's original startup path, compatibility layer, driver and resolution. Close the game normally. Back up locally before modifying a prefix. Never upload that backup: it may contain account identifiers, registry data or other private content.

## 2. Install and update the game

Use your own Battle.net account and authorized game installation. Confirm that the ARM64 client build matches the available service. During testing, build 69977 could reach login but did not list realms while the PC installation was on 70009; updating the handheld installation removed that build mismatch.

Do not redistribute the client or supply authentication tokens.

## 3. Prepare an isolated runtime and prefix

Clean bootstrap has passed a device probe without copying the owner's prefix:
create the empty directory, create C:/Z: mappings, seed matching runtime ntdll
and cryptbase (including the runtime's i386 cryptbase for syswow64), then run
wineboot with optional mscoree/mshtml disabled during bootstrap only. Check
the return codes, registry files and DLL equality, not just directory presence.
The extracted implementation is `installer/create-prefix.sh`.

The generalized installer completed in a separate environment on the owner's
device, and gameplay and gamepad-settings persistence passed manual testing.
The final-folder flow, direct entry and restart also passed. Do not publish the
owner's prefix archive. See VALIDATION.md for the packaging-only tar change.

Record the exact Wine source revision, full patch set and build inputs. The tested runtime includes the ARM64 syscall/TEB work, the NLS allocation fix, Android SysV shared-memory support, matching `cryptbase`, and matching Windows-visible `ntdll.dll`. Establish which changes belong to the upstream fork and which are local; a short commit ID is not a complete source manifest.

Install native Windows ARM64 DXVK 2.4.1 into this separate prefix. Do not substitute x64 DLLs or assume that ARM64EC packages are interchangeable with plain ARM64 DLLs.

## 4. Stage the driver and scoped GL workaround

Build Turnip at the pinned revision with `patches/turnip-kill-local-baryf.patch`. The successful artifact uses Android API 28, KGSL, NDK r27d and disabled Mesa shader cache. The historical Windows-host build also needed generator/lexer portability adjustments; those must be captured before claiming reproducible builds.

The no-OpenGL shim must be visible only to the dedicated game process through its library search path. Keep the Vulkan driver available. The tested launch also retained a native assertion tracer; removing that diagnostic dependency has not been tested yet.

## 5. Parameterize paths

The installer discovers a single standard game/container path and refuses
missing or ambiguous matches. Custom-folder selection is not implemented.
Never ship a personal container UUID or removable-storage identifier. Preserve
inherited GameHub sandbox-related environment variables.

## 6. Launch profile

Seed the custom configuration only if it does not exist. Use the included
`Config-Thor-Forever.wtf` starter profile (graphics quality 0, raid quality 2,
VSync 0 and a 30 FPS cap). Its complete graphics settings resolved the observed
menu artifact in testing; no single setting was established as the cause.
Preserve the tested allocator/narration workarounds. Do not rewrite the
configuration at every launch.

The working command's game arguments are:

```text
-d3d11 -config Config-Thor-Forever.wtf
```

Use an atomic directory lock to avoid concurrent sessions. A previous external `flock` implementation failed because its file descriptor did not survive the GameHub process wrapper.

## 7. Direct GameHub entry

Use the **same existing container's** General → Startup File Path to select the dedicated Windows launcher, not the game executable or Battle.net installer. The tested wrapper calls a shell bridge; that bridge calls the proven game launcher, writes a completion marker and redirects stdin/stdout/stderr. The Windows wrapper stays alive until completion.

The unmodified `start.exe /wait /unix` approach was not sufficient in this environment. A second attempt exited with status 141 until standard streams were redirected. These are observed outcomes, not proof of every internal GameHub lifecycle detail.

## 8. Acceptance tests before release

- Cold-start the container and reach login via the GameHub entry.
- Enter a realm and play; measure frame times if publishing performance claims.
- Enable gamepad, remember account, exit through the game menu and relaunch twice.
- Confirm settings survive and original Battle.net/container settings remain usable.
- Confirm a second launch is rejected while the first is active.
- Test recovery after device reboot and after an interrupted launch.
- Repeat on a fresh isolated prefix; document all required dependencies and hashes.
- Provide a tested rollback that does not delete games, saved variables or personal prefixes.
