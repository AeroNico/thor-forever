# Technical findings and evidence limits

## Turnip compiler

The final patch changes `check_instr` in `src/freedreno/ir3/ir3_sched.c`. During kill/demote scheduling, ignore `baryf` instructions whose block is not the block currently being scheduled. Local unscheduled varying fetches must still block scheduling.

A local offline compiler harness exercised the real Turnip frontend, descriptor/I/O lowering and IR3 compiler with a reconstructed descriptor layout and an Adreno 740 profile. It was not an exact replay of the game's complete captured pipeline state.

Final paired corpus results: baseline 491 successful shaders and one failure; patched 492 successful shaders and zero failures; no timeouts in either final run. The earlier `could_sched` hypothesis did not resolve the captured failure and is **not** part of the final patch. Captured game shaders are deliberately excluded from this repository.

The successful stripped Android artifact had SHA-256:

```text
51c1b2c9d4c124923bbdc6fcf182629ca447dd20110bca0f1bae4aac12481401
```

That identifies the historical artifact only. It is not a download link, a signature, or a promise that another build will be byte-identical.

## Separate GLX failure

Native tracing identified a `driQueryOptionb` assertion in GameHub's `libgallium-25.1.4.so`, reached through Mesa GLX during Wine window initialization. This was distinct from the Turnip shader failure. For this D3D11/Vulkan launch, a scoped `libGL.so.1` with no OpenGL API caused Wine's checked lookup to report OpenGL unavailable instead of initializing that path. It is inappropriate for applications that need OpenGL.

## Settings persistence

Before correction, both the custom configuration and default configuration remained unchanged across a recorded normal game exit (`WOW_EXIT=0`). Unix permission checks reported writable files and directories. This did not exhaustively test every Windows access-control or file-I/O condition.

The only final launcher change was replacing `-config 'WTF\Config-Jugabilidad-01.wtf'` with `-config 'Config-Jugabilidad-01.wtf'`. The owner then reported persistence working. We did not capture an internal file-I/O trace proving the precise reason the former spelling failed to save.

## Performance

The owner described the final low-quality, 30 FPS profile as very playable. Earlier input stalls also affected keyboard input while rendering looked fluid. No controlled input-latency benchmark was performed; do not claim that a particular driver fix eliminated all input problems, or advertise guaranteed FPS.
