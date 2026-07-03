# Unreal MCP Setup Guide

This document describes the MCP prerequisite for using `superpowers-game-extension` with Unreal Editor control.

This extension does not install or enable Unreal MCP directly. To let an AI agent inspect or control the Unreal Editor, first configure Unreal MCP in the target Unreal project using Epic's [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) documentation.

Korean version: [UNREAL_MCP_SETUP.md](UNREAL_MCP_SETUP.md)

## Why this comes first

`superpowers-game-extension` installs game development workflow rules, living docs, and safety guidance. Unreal MCP is what gives an AI agent access to editor functionality such as levels, actors, Blueprints, Slate widgets, and automation tests.

Without Unreal MCP, documentation and code work can still happen, but editor-state inspection and automation are limited.

## Source

- [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor)

Epic's documentation describes Unreal MCP as an MCP server embedded inside the Unreal Editor process. It lets MCP-compatible AI agents drive editor functionality over a local HTTP connection. The feature is experimental, so use caution around shipping workflows.

## Setup

1. Open the target Unreal project in Unreal Editor.

2. Enable the Unreal MCP and AllToolsets plugins.

   ```text
   Edit > Plugins
   ```

   Search for `Unreal MCP` and enable it. The `Toolset Registry` plugin is enabled automatically as a dependency.

   Then search for `AllToolsets` and enable it too. Unreal MCP provides the server connection, while `AllToolsets` provides the editor toolsets/tools. If `AllToolsets` is disabled, the agent may connect but have no useful toolsets or only a very limited set.

   Restart the editor if prompted.

3. Configure Auto Start Server.

   ```text
   Edit > Editor Preferences > General > Model Context Protocol
   ```

   Enable `Auto Start Server` to start the MCP server when the editor launches. The default endpoint is:

   ```text
   http://127.0.0.1:8000/mcp
   ```

   If needed, adjust the port and URL path in the same preferences panel.

4. Start the server manually if Auto Start is disabled.

   Run this in the editor console:

   ```text
   ModelContextProtocol.StartServer
   ```

   To specify a port:

   ```text
   ModelContextProtocol.StartServer 8000
   ```

5. Generate AI client configuration.

   In the editor console, specify the desired client:

   ```text
   ModelContextProtocol.GenerateClientConfig Codex
   ```

   To configure multiple agents at once:

   ```text
   ModelContextProtocol.GenerateClientConfig All
   ```

   Epic's documentation lists `ClaudeCode`, `Cursor`, `VSCode`, `Gemini`, `Codex`, and `All` as supported client names. JSON-format configs are merged with existing entries, while the Codex CLI TOML config can be write-once; stale Codex config may need manual cleanup.

6. Start your AI coding agent from the project/workspace root where the config was generated.

7. Verify the connection.

   Ask the agent for a read-only check first:

   ```text
   Verify the Unreal MCP connection and inspect the current toolsets, editor state, and open level without changing the project.
   ```

   If `list_toolsets` is empty or much smaller than expected, re-check that the `AllToolsets` plugin is enabled.

## Expected result

After setup, an AI agent should be able to:

- verify the MCP server connection
- list toolsets and tools provided by `AllToolsets`
- inspect level, actor, Blueprint, UMG/CommonUI, and material state
- run read-only checks for automation tests or editor state
- capture project/level state before mutating tool calls

## Safety rules

- Start with read-only checks.
- Treat Unreal MCP tool calls as serialized game-thread work and avoid overlapping calls.
- Do not directly text-edit binary engine assets such as `.uasset` or `.umap`.
- Treat the local MCP endpoint as an unauthenticated local development endpoint and do not expose it to the network.
- Unreal MCP and toolset APIs can change, so ask the agent to inspect the current toolset/schema first.

## Relationship to this extension

After Unreal MCP is configured, ask an AI agent to read [INSTALL_FOR_AI.md](INSTALL_FOR_AI.md) and install `superpowers-game-extension` into the target Unreal project.

```text
Read INSTALL_FOR_AI.md from WackyGameStudio/SuperpowersGameExtension and install it into this Unreal project.
```
