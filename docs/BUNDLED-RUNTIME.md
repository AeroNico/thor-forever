# Bundled runtime audit

This is a packaging record, not a claim of validation on another handheld.
No installed files on the owner's device were changed by this audit.

## Unused prefix-import files

The original Wine archive contains `prefixPack.txz` and `profile.json` for
upstream container import. Thor Forever's installer does not read either file;
`create-prefix.sh` initializes a new prefix instead. The nested prefix archive
contains 74 executable/DLL files from a separate upstream build and is not the
owner's prefix. Its redistribution/source history has not been established here.

Rather than include unused executables, `tools/prepare-runtime.py` excludes
exactly these two top-level files from a new archive. It does not delete or
modify the original archive, installed prefix, game files, or device data.

| Archive | SHA-256 |
| --- | --- |
| Original tested Wine tar | `41d22dca5c6ede633e59971f16bf180e449583648b4c804027e23353cce1a453` |
| Public-packaging Wine tar | `23c36158198eeb4d7037f6ef060b5ffabc692013822857fb9ae27b3a301891ca` |

All **2,589 retained members** were compared for identical contents, type,
permissions, ownership fields, timestamps, size and link targets. This preserves
the working runtime libraries; it is not a Wine update. Device acceptance was
performed with the original tar. The public-packaging tar has this additional
host-side equivalence check, not a separate device-installation claim.

## Supporting libraries and notices

| Component | Evidence | Notice included |
| --- | --- | --- |
| libdrm | Both bundled and Termux 2.4.134 `libdrm.so` are byte-identical. | `notices/LIBDRM.txt` |
| Wayland client/EGL | Both libraries are byte-identical to Termux 1.25.0-1. The fork's `wayland-client.pc` says 1.26.0, but the binary comparison agrees with `TURNIP.md` (1.25.0). | `notices/WAYLAND.txt` |
| xkbcommon / xkbregistry | Both bundled pkg-config files identify 1.13.1. Upstream 1.13.1 source and LICENSE preserved. Current Termux 1.13.2 binaries are not a match and are not substituted. | `notices/XKBCOMMON.txt` |
| xkeyboard-config | Fork documentation attributes the data to Termux 2.48-1. Of 293 regular package files mapped to the runtime layout, 218 are identical and 75 differ; do not call the entire tree a byte-identical copy. The exact shipped tree is preserved in the pinned Wine fork source. | `notices/XKEYBOARD-CONFIG.txt` |
| Banners-Turnip recipes and patches | Exact snapshot `0121416358dce37615bb3ff97e67980ce7baf353`; root license is GPL-3.0, not Thor Forever's MIT license. | `notices/BANNERS-TURNIP-GPL-3.0.txt` plus source notices |

Reference packages were downloaded from the official
[Termux repositories](https://packages.termux.dev/). They were inspected as
archives, not installed. Their SHA-256 values are:

```text
0cbe82140cf325c15473fbf53a3711fc7a2fb88e36a3eea58a3267c461ab4a17  libdrm_2.4.134_aarch64.deb
1f98af1db541027082b57998a6cd62da0c73701d656210c41283f77cccfb3ed6  libwayland_1.25.0-1_aarch64.deb
5e7317d47130aee16d8e18014423f1b1ab23601ca57cea81cd160ec4c1424167  xkeyboard-config_2.48-1_all.deb
aeb951964c2f7ecc08174cb5517962d157595e9e3f38fc4a130b91dc2f9fec18  xkbcommon-1.13.1.tar.gz
ac5e74d157830eb8bee44c6a6bf3ad49774ef0dd2a72bdad74a8f20308b52a95  libdrm-2.4.134.tar.xz
```

The xkbcommon source is from the [upstream tagged source](https://github.com/xkbcommon/libxkbcommon/tree/xkbcommon-1.13.1).
License notices copied from packages are converted to UTF-8 without changing
their text. A notice inventory is separate from a reproducible-build claim.

## Additional Mesa sources preserved

These are the additional Wayland drivers and EGL/GLES/Gallium sources bundled
by the Wine fork, not the separately patched `fe067b17` game driver. The six
archives below have been downloaded, parsed as valid tar archives, and checked
for their expected revision-named roots. Build patches are in the pinned
Banners-Turnip snapshot and the Wine fork's `android/wayland-deps/TURNIP.md`.

| Variant | Mesa revision | Source archive SHA-256 |
| --- | --- | --- |
| Base / EGL / GLES / Gallium | `7cda7850edd103ace21aac37d416d2fdf7a282e1` | `aa7a338064a10ce4db4a729a15204b748f0ae5e8fa80aa2341840127f3f38f93` |
| a7xx | `7631b5254f1a0a4371f5594e630ce2f2b8394e73` | `39103b7fe47ffd930ec0abcdc9b6847b8f3c5187b395ab6dc52d006d0245f976` |
| a8xx / perf / gen8 | `12b7b819edb4ddd3580e7e5ffe384610ae726c90` | `9cf1b8959d35bbaa6a35ea0e6bba09bce5970c399ccec090b51bbdb0cfe24582` |
| smxz | `c501e1d16e11c256610cd5922b1afa5660f2f5ea` | `dac01a757d1535ee2e243fa70ba92b5232f73091235dcb06dbf3c4773cfd833d` |
| white | `9c475fc367a7283a7eee58501fb48149780f2c1e` | `a3d1b88f7225a7eb9daff0b725965143b37447443cb480db3295b4ec7af551cd` |
| upstream | `bbc7792f717f27b17b4c12e6a4503d703a362aac` | `2bf5207a17a7ba270839edcdfa63f8a77bd5446c90ee2988db3f6f2100dff3c7` |

Archive origin: `https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/REVISION`,
except white, which uses `whitebelyash/mesa-unified`. The former is a mirror of
the upstream Mesa repository. Preserve the full upstream source notices in the
source distribution rather than labeling all variants as MIT-only.

## Remaining publication work

Assemble and inspect the downloadable source companion and binary kit together.
The Wine source snapshot itself vendors prebuilt libraries, so it must not be
advertised as a binary-free source archive without filtering those entries.
Retain build recipes, patches and per-source notices. The successful private
candidate and the files above do not, by themselves, constitute a published
downloadable release.
