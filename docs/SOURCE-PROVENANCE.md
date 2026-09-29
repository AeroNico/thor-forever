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
Submodules and third-party header notices still require a release inventory.

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
A beginner-ready installer remains blocked on the dependency package and final
portable launcher, even though private installation and gameplay have passed.

### Additional libraries found inside the Wine runtime

Archive inspection found eight Wayland Turnip variants, libgallium, EGL/GLES,
Wayland, xkbcommon/xkbregistry and libdrm in `lib/`. They are additional upstream
components, not covered simply by naming Wine's LGPL license. The fork records
their build lineage in `android/wayland-deps/TURNIP.md`, including Banners-Turnip
Wayland build `0121416` and per-driver Mesa pins. Matching source archives,
dependency notices and the full corresponding-source bundle must accompany a
binary release. Do not confuse our separately patched driver with these bundled
variants. They have not been removed from the tested runtime.
