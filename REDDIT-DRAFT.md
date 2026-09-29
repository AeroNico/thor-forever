# Draft — do not post until the installation kit is validated

Title: WoW Forever Beta on AYN Thor: working gameplay, direct GameHub launch, and saved settings

I got the ARM64 Forever Beta client running on my AYN Thor through GameHub Lite Ludashi. After testing, it is very playable for me with low graphics, 1280×720 and a 30 FPS cap. This is one device's experience, not a guaranteed performance claim.

The setup uses a separate patched Wine 11 runtime/prefix, ARM64 DXVK and a Turnip scheduler patch. There was also a separate GLX initialization issue that needed a scoped workaround. The original Battle.net/GameHub components were kept intact.

Two details that mattered at the end:

- Direct launch needed a wrapper that stayed alive while the shell/game ran, with the shell's standard streams redirected.
- Passing the custom settings filename without the `WTF\` prefix fixed persistent settings in my test. Gamepad preferences and the remembered account now survive restarting the game.

I worked through the debugging with ChatGPT/Codex and tested the changes on the handheld. Credit also goes to the Wine, DXVK, Mesa/Turnip and GameHub Lite developers, and u/BryTheGuy06 for the community guide/comment that started this investigation.

Guide, source, limitations and rollback: https://github.com/AeroNico/thor-forever

Publication check: the URL above is the approved target. Verify that the
repository and a usable release exist before posting this draft.

You need your own authorized game installation and eligible account. No game files, accounts or personal prefixes are included. Please read the tested-version list before trying it; this is experimental and game updates may break compatibility.
