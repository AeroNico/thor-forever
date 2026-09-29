# Source provenance and remaining release work

This inventory is not a declaration that all binary redistribution requirements
are complete. No third-party binaries are included in this source snapshot.

## Wine Android runtime

Repository: https://github.com/AeroNico/proton-wine

Confirmed revision: `52796bf615c265c23b22ae9dacc3da9e38c8487f`.
Its parent is `dbae574ca0c0d3136ad644e6b9dd108bc9dce193`.
The public commit changes only `android/patches/server_unicode.c.patch`.
It replaces an undersized path allocation with `asprintf` and updates the
patch hunk. Do not substitute the parent revision for this runtime's source.

Build recipe to review at that revision:
`.github/workflows/build-proton-11.0-1.yml` and its referenced Android scripts.
The tested payload is the extracted runtime tar, not merely the downloaded
GitHub artifact wrapper. Its hash is recorded in DEPENDENCIES.md.

Included notices: `notices/WINE-LICENSE.txt` and `WINE-COPYING.LIB.txt`, copied
from the local parent checkout. The reviewed commit does not change those files.
Before a binary release, preserve corresponding source, build inputs, submodule
revisions and applicable notices for bundled dependencies; a GitHub link alone
is not our completed source-distribution package.

## DXVK

Repository: https://github.com/doitsujin/dxvk

Revision: `0cf05780abd7250c2cd713b7749cf32180157cf5` (2.4.1).
The local altered source is marked by `patches/dxvk-arm64-toolchain.patch`.
The tested build also force-includes `<algorithm>` using the compiler options
`-include algorithm`. This compiler option must be preserved when reproducing
the historical build. The copied upstream license is in `notices/DXVK-LICENSE.txt`.
Submodule pins and third-party header notices are recorded in BUILDING.md and
the DirectX, SPIR-V and Vulkan notice files.

## Mesa / Turnip

Revision: `fe067b17d908d8f02e88ef3c4433ec5fbb66b2a9`.
The functional scheduler change is `patches/turnip-kill-local-baryf.patch`.
The successful Windows-host build also required generator/lexer adaptations,
now recorded in `patches/mesa-windows-host.patch`. Comparison with the original
source archive found only three changed source files: those two build files and
the scheduler. Python cache files are excluded from source distribution.
Mesa has multiple component licenses. Do not label the entire driver as covered
by Thor Forever's MIT license or include only a generic MIT notice.

## Android shared-memory support

Source: the Wine fork's `android/android_sysvshm` directory. Source hashes are
recorded in DEPENDENCIES.md. The C file credits a basis in
https://github.com/pelya/android-shmem. Its header lacks a license statement;
the upstream android-shmem BSD-3-Clause notice has now been retrieved and
preserved in `notices/ANDROID-SHMEM-LICENSE.txt`. Retain the Wine fork's source
and notices for its version, rather than attributing all changes to that upstream.

## Original diagnostic helpers

The sources `src/no-opengl-shim.c` and `src/graphics-assert-trace.c` are original
MIT-licensed helpers. The latter records fatal assertions and forwards them;
it is not an assertion bypass. It remains in the tested launch environment.
Neither helper justifies distributing game assets or captured shader files.

## Publication boundary

The source snapshot intentionally excludes the private test package, all game
files, personal prefixes, logs, account settings, compiler bundles and binaries.
The final-folder launcher, installation, gameplay and gamepad persistence have
passed on the owner's device. The experimental release supplies a separate
source companion; see SOURCE-DISTRIBUTION.md. Independent-device validation
and independent rebuilds are not claimed.

### Additional libraries found inside the Wine runtime

Archive inspection found eight Wayland Turnip variants, libgallium, EGL/GLES,
Wayland, xkbcommon/xkbregistry and libdrm in `lib/`. They are additional upstream
components, not covered simply by naming Wine's LGPL license. The fork records
their build lineage in `android/wayland-deps/TURNIP.md`, including Banners-Turnip
Wayland build `0121416` and per-driver Mesa pins. Component-specific notices and
source distribution materials are tracked in BUNDLED-RUNTIME.md.
Do not confuse our separately patched driver with these bundled
variants. They have not been removed from the tested runtime.

Preserved source archives now downloaded and hashed locally:

| Source | Revision | Archive SHA-256 |
| --- | --- | --- |
| Wine fork | `52796bf615c265c23b22ae9dacc3da9e38c8487f` | `1e4af10a578c8a7d1075f9cdbf68d02adc5302fd956b42e452d6eb44503f0531` |
| Banners-Turnip build recipes | `0121416358dce37615bb3ff97e67980ce7baf353` | `6fa5d717bd93423867b696cff3ceb78ac1c9521c5b03daa092a1772c43700196` |
| Wine directaudio submodule | `2101085596ffe4911f7686012a97585eacbde9d0` | `f16bee1ba4864cad3ebcc704d02b31cefeecbd21fbd7e713bb3fa08f354c3408` |
| DXVK | `0cf05780abd7250c2cd713b7749cf32180157cf5` | `64b1c768dbff87cf7bbea6803502826491293be7a533d3079b8da69e1e7f0aa0` |
| DirectX headers | `9df86f2341616ef1888ae59919feaa6d4fad693d` | `9c1b8bbfd2d6c758fac4d93c2808a46bc1eee429fe656b4f21b29e02615aa8aa` |
| SPIR-V headers | `8b246ff75c6615ba4532fe4fde20f1be090c3764` | `cfeed5f9a97d12a9761a26e7f5bd10fedb1a8ce92033075151ae3bc7206fc229` |
| Vulkan headers | `46dc0f6e514f5730784bb2cac2a7c731636839e8` | `322c947754bae5e3cdca3b21aba20f420569f14e4784b20cdbc7565e2b593734` |

Wine's directaudio submodule is pinned to
`2101085596ffe4911f7686012a97585eacbde9d0` in
https://github.com/The412Banner/directaudio. A GitHub source tar does not itself
populate that submodule. Preserving the parent tar is therefore not sufficient
to claim a complete recursive source bundle. Both parent and submodule archives
are included separately. Downstream bundled dependencies and notices are
inventoried in BUNDLED-RUNTIME.md and SOURCE-DISTRIBUTION.md.
