# superpowers-game-extension

`superpowers-game-extension` is a repo-local extension that adds game development context to `Superpowers`.

This repository does not modify the global `obra/superpowers` workflow. Instead, it installs `AGENTS.md`, `.agents/skills`, and `docs/game` templates into a Unity or Unreal game project so an AI agent can follow game-specific documentation, engine checks, and verification practices inside the normal `Superpowers` flow.

Korean version: [README.md](README.md)

## Why this exists

`Superpowers` is useful as a general development workflow that moves from brainstorming to design/spec, plan, implementation, and verification. Game development needs more context than code changes alone.

Game work often depends on Unity/Unreal editor state, scene/level structure, asset imports and references, playtest results, performance budgets, input/camera feel, save data, and localization/accessibility constraints. With a generic workflow only, an AI agent can miss engine/editor state, let project docs drift away from implementation, or handle MCP/Editor operations without enough safety checks.

This extension exists to close that gap.

## How it helps

Installing the extension adds repo-local rules, game skills, and living docs templates to the target game project.

```text
GameProject/
  AGENTS.md
  .agents/skills/
  docs/game/
```

Users can keep asking for work in the usual `Superpowers` flow. For example, when a request moves from brainstorming through implementation and verification, the installed `AGENTS.md` and `SKILL.md` descriptions guide `instruction-based activation` of the relevant game skills.

The extension focuses on two things:

- It keeps `docs/game` living docs updated so people and AI agents can read the same game design, implementation state, and validation evidence.
- It connects Unity/Unreal MCP workflow and safety rules to editor-state checks, read-only probes, approval before mutating actions, and verification evidence.

This repository does not install Unity/Unreal MCP itself. Engine integrations such as MCPForUnity or Unreal MCP are configured separately in the target game project.

## Quick Start

1. If editor control is needed, configure engine MCP first. This must be done before an AI agent can read Unity/Unreal Editor state or control editor workflows such as scenes, actors, assets, console output, and tests.

   - Unity project: [Unity MCP Setup Guide](UNITY_MCP_SETUP.en.md)
   - Unreal project: [Unreal MCP Setup Guide](UNREAL_MCP_SETUP.en.md)

2. Open the target Unity/Unreal project and ask your AI coding agent to read [INSTALL_FOR_AI.md](INSTALL_FOR_AI.md) and install the extension:

```text
Read INSTALL_FOR_AI.md from WackyGameStudio/SuperpowersGameExtension and install it into this game project.
```

The AI agent will safely copy files from `template/` into the target project. If the target project already has `AGENTS.md`, it should preserve the existing content and append the game extension instructions below it.

3. After installation, ask for work as you normally would with `Superpowers`.

```text
Help me take this Unity project's combat loop from brainstorming through an implementation plan.
```

```text
Review the HUD flow in this Unreal project and update the relevant docs and validation steps.
```

Without MCP setup, documentation and code work can still happen, but editor-state inspection and automation are limited.

## What gets installed

The source of truth for the install payload is this repository's `template/` directory.

```text
template/
  AGENTS.md
  .agents/skills/
  docs/game/
```

The installer creates these files and directories in the target game project.

| Path | Purpose |
|---|---|
| `AGENTS.md` | Identifies the repository as a game project and guides local game skill selection across Superpowers stages. |
| `.agents/skills/` | Local skills for Unity/Unreal, scene/UI, assets, performance, save data, input/camera, AI, networking, and localization/accessibility work. |
| `docs/game/` | Living docs templates for game design, systems, scenes, UI flow, asset policy, architecture, save model, QA, performance, and release constraints. |

The AI installation flow is non-destructive by default. If the target project already has `.agents/skills` or `docs/game` files at the same paths, the agent should report conflicts instead of overwriting them. This extension repository's own root does not contain `.agents/` or `AGENTS.md`; that root safety constraint prevents local skills under development from being auto-loaded into the current Codex session.
With the `INSTALL_FOR_AI.md` flow, `AGENTS.md` is the only append-only special case. `.agents/skills` and `docs/game` should not be overwritten; the AI agent should copy only missing files or report conflicts.

## How to use it

Users do not need to memorize game skill names. The installed `AGENTS.md` adds game-domain routing to normal `Superpowers` stages.

| Superpowers stage | What the extension adds |
|---|---|
| brainstorming | Checks game design, UI, scene, asset, save, performance, input, AI, networking, accessibility impact, and related docs. |
| design/spec | Connects game rules, UX flow, engine constraints, and validation methods to living docs. |
| writing-plans | Adds docs updates, editor/MCP preflight, validation evidence, and rollback tasks to the plan. |
| implementation | Applies the local skill instructions that match the files, engine, and game domain being changed. |
| verification | Looks beyond compile/test and asks for fresh evidence such as playtest results, editor logs, screenshots, and docs updates. |

In short, keep using `Superpowers` normally. This extension adds local instructions for the documentation and engine/editor safety checks that game work often needs.

## Unity/Unreal MCP and safety rules

Unity/Unreal MCP is a local editor automation surface. This extension does not install MCP directly; it connects MCP usage to game workflow order and safety expectations.

The default principles are:

- Confirm that the editor is running and the correct project/instance is active.
- Prefer read-only queries and current-state snapshots before mutating tool calls.
- Do not directly text-edit binary engine assets; prefer the editor, MCP, commandlets, or documented engine tooling.
- When multiple Unity Editor instances or Unreal MCP toolsets exist, state the target project and toolset explicitly.
- Treat local MCP endpoints as localhost-only and do not expose them to the network.

When MCPForUnity is installed in a Unity project, it creates `.codex/skills/unity-mcp-skill/SKILL.md`, whose frontmatter name is `unity-mcp-orchestrator`. This extension's Unity workflow coordinates with that local skill pack for game docs, scene/UI safety, and validation evidence.

## Living Docs

`docs/game` is a living docs set for people and AI agents to share. When game rules, UX flow, scene structure, system architecture, engine integration, QA, performance budgets, or release constraints change, the related docs should be updated in the same task.

The default document map is:

- `00-index.md`: project identity, document map, current validation status
- `01-vision-and-pillars.md`: target experience, design pillars, non-goals
- `02-core-loop.md`: core loop, session loop, reward loop
- `03-player-and-controls.md`: player verbs, input mapping, camera state, accessibility controls
- `04-gameplay-systems.md`: combat, AI, progression, multiplayer authority, validation path
- `05-scenes-and-levels.md`: scenes, levels, maps, transitions
- `06-ui-ux-flow.md`: HUD, menus, modal stack, routing, focus behavior
- `07-content-and-assets.md`: asset taxonomy, naming, source/generated policy, reference integrity
- `08-technical-architecture.md`: runtime modules, editor tools, engine integration
- `09-data-and-save-model.md`: save schema, migrations, compatibility, save/load validation
- `10-playtest-and-qa.md`: smoke tests, bug reproduction, validation evidence
- `11-performance-budgets.md`: target platform, frame/memory/loading budgets, measurement results
- `12-build-release-platforms.md`: build scenes/maps, packaging constraints, pre-release checks
- `decision-log.md`: important decisions and trade-offs
- `change-log.md`: game-meaningful changes

## Included game skills

The installed `.agents/skills` cover these game domains.

| Skill | Applies to |
|---|---|
| `game-docs-maintaining` | design, gameplay rules, scenes, UI flow, content, architecture, save data, testing, performance, build targets, project documentation |
| `game-engine-mcp-operating` | Unreal/Unity MCP connections, editor tools, engine-owned assets, scene inspection, editor state validation |
| `unity-mcp-workflow` | Unity MCP, Unity Editor automation, scenes, GameObjects, prefabs, ScriptableObjects, uGUI, UI Toolkit, Play Mode, Edit Mode tests |
| `unreal-mcp-workflow` | Unreal MCP, Unreal Editor automation, levels, actors, Blueprints, UMG, CommonUI, materials, PIE, Automation tests |
| `game-scene-ui-iteration` | levels, scenes, actors, GameObjects, prefabs, widgets, canvases, UIDocuments, menus, HUDs, visual hierarchy |
| `game-playtesting-and-validation` | gameplay verification, bug reproduction, Unity tests, Unreal Automation tests, smoke tests, editor log checks |
| `game-ui-implementation` | HUDs, menus, UI Toolkit, uGUI, UMG, CommonUI, navigation, focus, runtime UI binding |
| `game-asset-pipeline` | import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, asset naming/folders |
| `game-performance-budgeting` | FPS, frame time, hitches, memory, draw calls, shader cost, loading time, build size, profiling |
| `game-save-data-migrations` | save schema, persistence format, progression data, migrations, backward compatibility, save/load tests |
| `game-input-and-camera-design` | player controls, input mapping, Unity Input System, Unreal Enhanced Input, camera states, aiming, lock-on |
| `game-ai-behavior-debugging` | Behavior Trees, state machines, NavMesh, pathfinding, perception, blackboards, spawn logic |
| `game-networking-authority` | multiplayer authority, ownership, replication, prediction, rollback, matchmaking, deterministic tests |
| `game-content-branching-and-merging` | binary engine assets, asset locks, prefab/Blueprint conflicts, Unreal OFPA, Unity YAML conflicts |
| `game-localization-accessibility` | localization keys, translated text, font fallback, subtitles, readability, colorblind support, input accessibility, safe areas |

## Developer notes

This extension repository's own root does not contain `.agents/` or `AGENTS.md`. The install payload is always managed under `template/`. This constraint prevents a Codex session developing the extension from auto-loading local skills that are still being validated.

Codex plugin packaging is not the default install path yet. The current default path is to have an AI coding agent read `INSTALL_FOR_AI.md` and install repo-local `AGENTS.md`, `.agents/skills`, and `docs/game` into the target game project.
