# Dependency inventory

These are the experimental release payload hashes. Wine is repackaged without
two unused prefix-import files; its retained members are identical to the tested
runtime. See BUNDLED-RUNTIME.md and SOURCE-DISTRIBUTION.md. Binaries are release
assets, not files in this Git tree.

| Artifact | SHA-256 |
| --- | --- |
| Wine runtime tar (public packaging, unused prefix-import files omitted) | `23c36158198eeb4d7037f6ef060b5ffabc692013822857fb9ae27b3a301891ca` |
| ARM64 DXVK d3d11.dll | `7da6a1fc8d741abd5b0404eca7a99fdf490c832626a290fb31689c38f5a3bcae` |
| ARM64 DXVK dxgi.dll | `35af848fd7e316113c54a13af2fe7e14760383d236fe29a6b8cd18f09e9c1f4e` |
| Android libandroid-sysvshm.so | `8aba6a640a60783e8c882066d3cd49e5155b07fc7e1a5dd0aa7009cef369465a` |
| Patched libvulkan_freedreno.so | `51c1b2c9d4c124923bbdc6fcf182629ca447dd20110bca0f1bae4aac12481401` |
| Scoped libGL.so.1 | `df76b24dd14b77e56727864702c4a589ebedb609bdf3bfdaefa30863101a9e8f` |
| Assertion tracer trace.so | `82fc90739eadfbbe053d51ce18e3d1bdde4bcda5f204dfbfe3c6b5658027e319` |

DXVK source: version 2.4.1, revision
`0cf05780abd7250c2cd713b7749cf32180157cf5`. Local compiler compatibility
adjustments explicitly include `<algorithm>` and construct the default pipeline
key for a tuple; these must be supplied with reproducible build instructions.
Target: Windows ARM64 (not x64), llvm-mingw 20260922 UCRT, glslang 16.6.0.

Turnip source revision and the scheduler patch are described in TECHNICAL-NOTES.
Build: NDK r27d, Android API 28, KGSL, no OpenGL, static C++ runtime, shader cache
disabled. Windows-host generator/lexer adaptations are included in
`patches/mesa-windows-host.patch`.

Shared-memory source was taken unmodified from the Wine Android fork's
`android/android_sysvshm`. The exact C source hash is
`cc58b9a7e7ccec14fa1193418b4760c3aa871ae1fbbc55eef25f30b7f7ee6b86`;
header hash is `a87ea260794e6fae3820d7004916fce27e0d396ae266a3bb8b9e55bf08767609`.

Wine's source revision is now confirmed as
`52796bf615c265c23b22ae9dacc3da9e38c8487f`, whose parent matches the local
checkout `dbae574ca0c0d3136ad644e6b9dd108bc9dce193`. See SOURCE-PROVENANCE.md
and SOURCE-DISTRIBUTION.md for the companion archives and reconstruction notes.

The tested launch also uses a scoped OpenGL-unavailable shim and native assertion
tracer. Both original helper sources are included. Do not silently omit the
tracer from the tested launch environment. Independent bit-for-bit rebuild
verification remains outside this preview's validation claims.
