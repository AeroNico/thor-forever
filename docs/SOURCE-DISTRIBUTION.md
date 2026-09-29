# Source companion for v0.1.0-alpha.1

The release offers the installer and `Thor-Forever-v0.1.0-alpha.1-Sources.zip`
at the [same download location](https://github.com/AeroNico/thor-forever/releases/tag/v0.1.0-alpha.1).
The source companion is for developers and redistribution compliance; players
do not need to extract it onto the handheld.

## What is included

- Thor Forever installer, launcher/helper sources, tests, patches and notices.
- Wine at `52796bf615c265c23b22ae9dacc3da9e38c8487f`, including Android patches,
  shared-memory source, build scripts and its pinned workflow.
- The separate directaudio submodule snapshot needed by that Wine revision.
- DXVK 2.4.1 and the DirectX, Vulkan and SPIR-V header submodules used by the
  Windows ARM64 build. Optional libdisplay-info is not part of this Windows
  build; its recorded Git pin remains in BUILDING.md for reference.
- The game driver's Mesa source and Thor Forever's two Mesa patch files.
- Six additional Mesa source snapshots and Banners-Turnip's exact patch/build
  recipe snapshot for the Wayland drivers and EGL/GLES/Gallium bundled by Wine.
- libdrm and xkbcommon upstream source archives; the exact bundled keyboard
  data is in the Wine fork's `android/wayland-deps/usr/share/X11/xkb` tree.

`SOURCE-MANIFEST.json` records every included upstream archive's checksum,
original download URL and original checksum. Archives retain upstream license
files and per-file copyright notices. No root license overrides those notices.

The Wine source archive is filtered only to omit its 16 vendored prebuilt ELF
libraries. Their names and hashes are recorded in the manifest. Source code,
headers, keyboard data, patches and build recipes are preserved. Do not mistake
the filtered archive for a ready-made binary dependency directory.

Wayland client/EGL binaries are the unmodified Termux 1.25.0-1 libraries;
their MIT notice is included. Upstream source is available from
[Wayland's release page](https://wayland.freedesktop.org/releases.html).
Termux's [package recipes](https://github.com/termux/termux-packages) document
its Android integration. See BUNDLED-RUNTIME.md for binary comparison evidence
and the pkg-config version discrepancy.

## Reconstructing source trees

Extract each required upstream archive into its own directory. Place the
directaudio archive's contents into Wine's `dlls/winedirectaudio.drv`.
Place the three DXVK header snapshots at the matching paths listed in
BUILDING.md. Apply Thor Forever's DXVK patch and both Mesa patches to their
respective trees. Wine's NLS fix is already committed in its supplied source.
Do not apply the game-driver scheduler patch to the unrelated Wayland variants.
Their per-variant patches are in the Banners-Turnip snapshot instead.

Follow BUILDING.md and the supplied upstream build recipes for toolchain
versions and configuration. Compilers/SDKs are not bundled. This release does
not claim bit-for-bit reproducibility or a newly verified full rebuild on a
second machine. Rebuilt binaries require fresh validation, not just a renamed
archive. The prebuilt installer uses the pinned, device-tested component set.

## Repackaging the sources

With Python 3.11+, place the exact downloaded archives named in
`tools/package-sources.py` into one directory, then run:

```text
python -B tools/package-sources.py ARCHIVE-DIRECTORY NEW-SOURCES.zip
```

The tool rejects incorrect hashes and invalid tar archives, copies only the
allowlisted public project tree, refuses to overwrite an existing output, and
checks the resulting ZIP. It does not read game installations or device logs.

Keep this source companion, notices and checksums available with redistributed
binary copies, and comply with each component's license. Thor Forever imposes
no additional restriction on modifying or debugging the included free-software
libraries. GameHub and Blizzard software are not included or relicensed here.
