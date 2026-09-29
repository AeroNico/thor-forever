# Licensing scope

The MIT license in `LICENSE` applies to Thor Forever's original installer scripts,
original utility code, tests and documentation. The project's attribution uses
the owner's public GitHub handle, AeroNico.

It does not relicense Wine, Mesa/Turnip, DXVK, GameHub, Blizzard software,
third-party code or their assets. Changes to and excerpts from upstream source
must be distributed in accordance with that upstream component's applicable
license and notices. In particular, do not interpret the root MIT license as
relicensing the Mesa source context included in `patches/`.

No game files, personal prefixes or third-party binary release are included in
this source/documentation draft. Before distributing third-party binaries,
complete the dependency-specific source, license and notice checklist in
`docs/RELEASE-CHECKLIST.md`. A checksum alone does not fulfill those requirements.

The scoped no-OpenGL shim in `src/` is original utility code, not a copy of
Mesa's OpenGL implementation. Its inclusion does not grant rights to distribute
unrelated OpenGL libraries.
