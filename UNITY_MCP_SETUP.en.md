# Unity MCP Setup Guide

This document describes the MCP prerequisite for using `superpowers-game-extension` with Unity Editor control.

This extension does not install Unity MCP directly. To let an AI agent inspect or control the Unity Editor, first configure [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) in the target Unity project.

Korean version: [UNITY_MCP_SETUP.md](UNITY_MCP_SETUP.md)

## Why this comes first

`superpowers-game-extension` installs game development workflow rules, living docs, and safety guidance. Unity MCP is what gives an AI agent access to Unity Editor state such as scenes, GameObjects, assets, console output, and Play Mode.

Without Unity MCP, documentation and code work can still happen, but editor-state inspection and automation are limited.

## Source

- [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)

The CoplayDev README quickstart currently targets Unity 2021.3 LTS through Unity 6.x, requires Python 3.10+ with `uv`, and installs through Unity Package Manager before generating client configuration from Unity.

The CoplayDev README also documents `#main`, but this guide recommends pinning a release tag for reproducibility. At install time, check the latest stable release tag in [CoplayDev/unity-mcp Releases](https://github.com/CoplayDev/unity-mcp/releases).

## Setup

1. Open the target Unity project in Unity Editor.

2. Add the package through Unity Package Manager.

   Open `Window > Package Manager`, choose `Add package from git URL...`, and enter a URL pinned to a release tag:

   ```text
   https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<latest-release-tag>
   ```

   For example, as of 2026-07-03, the latest release is `v10.0.0`, so the URL is:

   ```text
   https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.0.0
   ```

   `#main` is a moving target that follows current development. For team projects or reproducible setup, use a release tag instead of `#main`.

3. Open the MCP for Unity window.

   ```text
   Window > MCP for Unity > Toggle MCP Window
   ```

   The window usually opens on the `Connect` tab the first time.

4. In the `Connect` tab, check server status and client configuration.

   - If the server is off, turn it on.
   - Configure the AI/MCP clients you want to use.
   - To configure all detected clients at once, use `Configure All Detected Clients`.
   - To use MCP for Unity's local skill pack, run `Install Skill`.

   When `Install Skill` succeeds, MCPForUnity installs its local skill into the Unity project. This extension's Unity workflow coordinates with that skill for `docs/game`, scene/UI safety, and validation evidence.

5. In the `Tools` tab, check tool exposure.

   The `Tools` tab manages the Unity Editor tools an AI agent can call. Tools are needed for agent-driven scene, GameObject, asset, console, and test operations.

   For initial setup with this extension, use `Enable All`. Teams can later narrow the enabled tools according to their safety policy.

6. In the `Resources` tab, check resource exposure.

   The `Resources` tab manages read-only Unity project/editor context an AI agent can fetch, such as project info, editor state, scene data, and camera data.

   For initial setup, use `Enable All`. Rich read-only context helps the agent inspect current state before making changes.

7. In the `Deps` tab, install dependencies.

   The `Deps` tab checks and installs dependencies required by MCP for Unity. This can include runtime pieces such as Python/uv or client/server support components.

   For initial setup, run `Install All`. If errors remain, follow the guidance shown for the failing dependency.

8. Leave the `Advanced` tab alone by default.

   The `Advanced` tab is for low-level settings and diagnostics. Keep defaults unless you specifically need to change port, transport, or other advanced behavior.

9. Start your AI coding agent from the target Unity project root.

   Running the agent from the Unity project root makes it easier for the client to find the generated MCP configuration.

10. Verify the connection.

   Ask the agent for a read-only check first:

   ```text
   Verify the Unity MCP connection and read the active scene, Play Mode state, and console errors without changing the project.
   ```

## Expected result

After setup, an AI agent should be able to:

- inspect the active scene and hierarchy
- query GameObjects, cameras, and UI objects
- read console errors and warnings
- run Play Mode/Edit Mode tests
- inspect editor state before changing scenes or assets

## MCP for Unity tab summary

| Tab | Purpose | Recommended initial setup |
|---|---|---|
| `Connect` | Manages MCP server on/off, client configuration, and skill installation. | Turn the server on, configure needed clients, and run `Configure All Detected Clients` and `Install Skill` when useful. |
| `Tools` | Manages editor tools the agent can call. | `Enable All` |
| `Resources` | Manages read-only project/editor context the agent can fetch. | `Enable All` |
| `Deps` | Manages dependency status and installation for MCP for Unity. | `Install All` |
| `Advanced` | Handles ports, transport, diagnostics, and other advanced settings. | Keep defaults |

## Safety rules

- Start with read-only checks.
- Before changing scenes, prefabs, or assets, ask the agent to state the change scope and rollback path.
- If multiple Unity Editor instances are open, specify the target project/instance.
- Treat MCP endpoints as local development endpoints and do not expose them to the network.

## Relationship to this extension

After Unity MCP is configured, ask an AI agent to read [INSTALL_FOR_AI.md](INSTALL_FOR_AI.md) and install `superpowers-game-extension` into the target Unity project.

```text
Read INSTALL_FOR_AI.md from WackyGameStudio/SuperpowersGameExtension and install it into this Unity project.
```
