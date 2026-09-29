# Thor Forever

**Status: documentation/source draft, not a ready-to-install release.**

The setup assistant is being developed for nontechnical users. A private package
has now installed a separate runtime, prefix and game layout on the owner's
AYN Thor. Gameplay, saved gamepad settings and direct GameHub launch passed
manual testing. The public source draft does not yet include a complete,
redistributable end-user package. See [validation results](docs/VALIDATION.md).

This project documents a working World of Warcraft: Forever Beta ARM64 setup on one AYN Thor, using GameHub Lite Ludashi, a separate patched Wine runtime, ARM64 DXVK and a locally patched Mesa Turnip driver. It is not affiliated with Blizzard, AYN, GameHub, Wine or Mesa.

The owner reports playable in-world gameplay, direct launch from GameHub, and persistent account-name/gamepad preferences after the final configuration-path correction. This is a single-device report, not a compatibility guarantee or a benchmark. Remembering an account name does not mean storing a password or bypassing authentication.

## Tested combination

| Component | Tested configuration |
| --- | --- |
| Hardware | AYN Thor, Adreno 740 |
| Android app | GameHub Lite Ludashi (`com.ludashi.aibench`) |
| Game | Forever Beta, ARM64 client, build 1.60.1.70009 |
| Runtime | Separate Android Wine 11 build with the fixes described below |
| Direct3D translation | DXVK 2.4.1, native Windows ARM64 DLLs |
| Vulkan | Turnip from Mesa revision `fe067b17d908d8f02e88ef3c4433ec5fbb66b2a9`, with a local scheduler patch |
| Starting profile | 1280×720, low graphics, VSync off, 30 FPS cap |

Versions describe the successful test, not current release recommendations. Later game updates may change compatibility. Obtain the game through authorized distribution and use your own eligible account.

## What made it work

1. Keep the original GameHub/Battle.net container intact. Prepare a separate Wine prefix and runtime; do not replace global components.
2. Use matching ARM64 runtime components, including the Windows-visible `ntdll.dll`, plus the required Android shared-memory support and ARM64 DXVK. A Wine version check alone does not establish that the game can run.
3. Correct an NLS path-allocation bug in the Wine Android patch set.
4. Patch Turnip's kill/demote scheduling check so that it does not wait for varying fetches belonging to another basic block. The captured failing shader compiled after this change.
5. Avoid an independent crash in GameHub's OpenGL/GLX initialization by using an isolated no-OpenGL shim for this launch. WoW uses D3D11 through DXVK/Vulkan. **Do not install this shim globally.**
6. Use the low-load profile. The owner reported much better playability and input responsiveness; we did not establish a single root cause for the earlier input stalls.
7. Use a persistent Windows launcher plus a shell completion marker for direct GameHub launch. Redirect the shell's standard streams before starting child processes.
8. Pass `-config Config-Jugabilidad-01.wtf`, **not** `-config 'WTF\Config-Jugabilidad-01.wtf'`. With the former, the owner confirmed settings and remembered account persisted after a normal exit and restart.

## Read before installing anything

Do not copy the historical troubleshooting scripts to another device. The new
installer discovers standard game locations and creates a fresh prefix, but
the final public launcher, third-party source/license package and complete
release workflow still need preparation. The private test folder is not a
public download and must not be uploaded as-is.

See [the setup and validation plan](docs/SETUP.md), [technical findings](docs/TECHNICAL-NOTES.md), [troubleshooting](docs/TROUBLESHOOTING.md), and [release checklist](docs/RELEASE-CHECKLIST.md).

For safe switching back to the original entry, see [recovery guidance](docs/RECOVERY.md).

This repository must not contain game files, account directories, an exported personal prefix, captured game shaders, raw logs, credentials, or third-party binaries without their source/license requirements addressed. Initial contents are documentation and selected source only.

## Credits and provenance

- Wine and the Android Proton/Wine work: [upstream fork used](https://github.com/The412Banner/proton-wine), [owner's build fork](https://github.com/AeroNico/proton-wine).
- Mesa/Freedreno/Turnip developers: source revision listed above.
- DXVK developers: ARM64 DXVK 2.4.1 used in the working setup.
- GameHub Lite maintainers, and [u/BryTheGuy06](https://www.reddit.com/user/BryTheGuy06/) for the original community guide/comment that motivated the investigation. This credit is not an endorsement of this project.
- Local investigation and implementation were carried out with assistance from ChatGPT/Codex, with the owner testing on the device.

Original Thor Forever code and documentation are licensed under [MIT](LICENSE).
Third-party work retains its own licenses; see [licensing scope](LICENSING.md).
The MIT license does not by itself authorize redistribution of third-party binaries.
