# INSTALL_FOR_AI.md

This file is a runbook for AI coding agents installing `superpowers-game-extension` into a Unity or Unreal game project.

Use this when a user says something like:

```text
Read INSTALL_FOR_AI.md from WackyGameStudio/SuperpowersGameExtension and install it into this game project.
```

## Goal

Install the contents of this repository's `template/` directory into the target game project so the project gets:

- game-aware agent instructions
- local game development skills
- `docs/game` living documentation templates

The install must be non-destructive. Preserve existing project files unless this document explicitly says to append.

## Required Inputs

Before changing files, identify:

- **Source extension root**: the cloned `SuperpowersGameExtension` repository.
- **Target game project root**: the Unity or Unreal project that should receive the template.

If the target root is unclear, ask the user for the exact directory.

Do not install into the extension repository itself.

## Source Files

Use `template/` as the source of truth:

```text
template/
  AGENTS.md
  .agents/skills/
  docs/game/
```

## Install Rules

### 1. `AGENTS.md`

Target path:

```text
<target-game-project>/AGENTS.md
```

Rules:

- If `AGENTS.md` does not exist, copy `template/AGENTS.md` to the target root.
- If `AGENTS.md` exists but is empty or whitespace-only, replace it with `template/AGENTS.md`.
- If `AGENTS.md` exists and has content, append the full contents of `template/AGENTS.md` below the existing content.
- Before appending, check whether the existing file already contains `Superpowers 단계별 game skill routing` or `superpowers-game-extension`. If it does, do not append a duplicate block; report that the instructions appear to be installed already.
- When appending, insert a clear separator:

```md

---

# superpowers-game-extension

```

Then append the body of `template/AGENTS.md`.

### 2. `.agents/skills`

Target path:

```text
<target-game-project>/.agents/skills/
```

Rules:

- If `.agents/skills/` does not exist, copy `template/.agents/skills/` there.
- If `.agents/skills/` exists, copy only missing skill directories.
- Do not overwrite an existing skill directory with the same name.
- If a skill directory already exists with the same name, report it as a conflict and ask the user before changing it.

### 3. `docs/game`

Target path:

```text
<target-game-project>/docs/game/
```

Rules:

- If `docs/game/` does not exist, copy `template/docs/game/` there.
- If `docs/game/` exists, copy only missing template files.
- Do not overwrite existing game docs.
- If a template file already exists with the same name, leave it unchanged and report it as already present.

## Verification

After installing, verify:

- `<target-game-project>/AGENTS.md` exists and includes the game extension instructions.
- `<target-game-project>/.agents/skills/` exists and includes the copied game skills or reported conflicts.
- `<target-game-project>/docs/game/00-index.md` exists or was reported as already present.
- No existing project file was overwritten without explicit user approval.

Report a short summary:

```text
Installed:
- AGENTS.md: created / appended / already present
- .agents/skills: copied N, conflicts M
- docs/game: copied N, already present M

Next:
- Open the target project with your coding agent.
- Use the normal Superpowers flow: brainstorming -> design/spec -> plan -> implementation -> verification.
- Configure Unity/Unreal MCP separately if engine/editor automation is needed.
```

## Agent-Specific Adaptation

`template/AGENTS.md` is the source instruction file. `template/.agents/skills/` is the source skill pack.

If the target agent supports `AGENTS.md`, keep `AGENTS.md` as the instruction file. If the target agent can use `.agents/skills/`, keep the skill pack there. Only create native copies for agents that do not load those paths.

Do not create symlinks unless the user asks for them. Plain file copies are easier to review and work better across Windows/macOS/Linux.

| Agent/tool | Instruction file handling | Skill handling |
|---|---|---|
| OpenAI Codex | Keep `AGENTS.md`. | Keep `.agents/skills/`. |
| GitHub Copilot coding agent / Copilot CLI | Keep `AGENTS.md`. Copilot also supports `.github/copilot-instructions.md`, but do not create it unless the user asks for a Copilot-only copy. | Keep `.agents/skills/` as the shared game skill/reference pack. Do not convert by default. |
| Cursor | Keep `AGENTS.md`. Cursor also supports `.cursor/rules/`, but do not create Cursor rules unless the user asks for Cursor-native rules. | Keep `.agents/skills/` as the shared game skill/reference pack. Do not convert by default. |
| Windsurf / Devin Desktop Cascade | Keep `AGENTS.md` or `agents.md`. | Keep `.agents/skills/` as the shared game skill/reference pack. Do not convert by default. |
| Cline | Keep `AGENTS.md`; Cline detects it. Do not create `.clinerules/` unless the user asks for Cline-native rules. | Keep `.agents/skills/` as the shared game skill/reference pack. Do not convert by default. |
| Claude Code | Create or append `CLAUDE.md` or `.claude/CLAUDE.md` with the installed `AGENTS.md` content, because Claude Code's native project memory is `CLAUDE.md`. | For native Claude Code skill activation, copy each `template/.agents/skills/<skill>/` directory to `.claude/skills/<skill>/` and verify each `SKILL.md`. If the user does not want native Claude skills, keep `.agents/skills/` only as reference. |
| Gemini CLI | Create or append root `GEMINI.md` with a concise version of the installed `AGENTS.md`, because Gemini CLI's native context file is `GEMINI.md`. | Keep `.agents/skills/` as reference material. Do not convert by default. |
| aider | Create or append `CONVENTIONS.md` with a concise version of the installed `AGENTS.md`; tell the user to load it with `/read CONVENTIONS.md` or `aider --read CONVENTIONS.md`. | Keep `.agents/skills/` as reference material. aider does not use `SKILL.md` directories as native skills. |

## References Checked

- OpenAI Codex `AGENTS.md`: <https://developers.openai.com/codex/guides/agents-md>
- OpenAI Codex skills: <https://developers.openai.com/codex/skills>
- GitHub Copilot custom instructions: <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions>
- Claude Code memory and `CLAUDE.md`: <https://docs.anthropic.com/en/docs/claude-code/memory>
- Claude Code skills: <https://docs.anthropic.com/en/docs/claude-code/skills>
- Gemini CLI `GEMINI.md`: <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html>
- Cursor rules: <https://cursor.com/docs/rules>
- Windsurf/Devin Desktop `AGENTS.md`: <https://docs.windsurf.com/windsurf/cascade/agents-md>
- Windsurf rules: <https://docs.windsurf.com/plugins/cascade/memories>
- Cline rules: <https://docs.cline.bot/customization/cline-rules>
- aider conventions: <https://aider.chat/docs/usage/conventions.html>
