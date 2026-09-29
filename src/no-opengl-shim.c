/* Scoped compatibility shim for a D3D11/DXVK/Vulkan launch.
 * Deliberately exports no OpenGL API. Wine's checked glGetString lookup
 * reports OpenGL unavailable rather than initializing the failing GLX path.
 * Never install globally or use for applications requiring OpenGL.
 * SPDX-License-Identifier: MIT */
const char wow_diagnostic_no_opengl[] = "Scoped diagnostic: OpenGL unavailable";
