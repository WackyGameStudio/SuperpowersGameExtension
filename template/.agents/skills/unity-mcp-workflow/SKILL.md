---
name: unity-mcp-workflow
description: Use when working with Unity MCP, Unity Editor automation, scenes, GameObjects, prefabs, ScriptableObjects, uGUI, UI Toolkit, Play Mode, or Edit Mode tests.
---

# Unity MCP Workflow

## Overview

Unity MCP 작업은 Unity Editor Plugin과 Python MCP server를 local editor automation surface로 다룬다. Scene, Prefab, `.meta` reference 안전성을 우선한다.

MCPForUnity를 설치하고 설정한 Unity 프로젝트에는 `.codex/skills/unity-mcp-skill/SKILL.md`가 생성되며, 이 skill의 frontmatter name은 `unity-mcp-orchestrator`다. `unity-mcp-workflow`는 게임 프로젝트 관점의 안전과 검증을 담당하고, MCPForUnity tool/resource 세부 절차는 `unity-mcp-orchestrator`와 그 references를 따른다.

## Workflow

1. `ProjectSettings/ProjectVersion.txt`, `Assets/`, `Packages/manifest.json` evidence로 Unity project를 확인한다.
2. Unity Editor가 대상 project를 열고 있는지 확인한다.
3. 여러 Unity Editor instance가 있으면 active instance를 고정한다.
4. MCP endpoint가 read-only query에 응답하는지 확인한다.
5. `.codex/skills/unity-mcp-skill/SKILL.md`가 있고 frontmatter name이 `unity-mcp-orchestrator`인지 확인한다.
6. MCPForUnity resource-first 흐름과 tool/resource 선택은 `.codex/skills/unity-mcp-skill/SKILL.md`의 `unity-mcp-orchestrator`를 따른다.
7. 기본 tool group 외에는 작업에 필요한 group만 `manage_tools`로 활성화한다.
8. Scene, GameObject, Prefab, Material, ScriptableObject, UI 변경 후 `refresh_unity`를 수행한다.
9. Console read, Edit Mode test, Play Mode test, scene validation 중 필요한 검증을 수행한다.
10. Scene/UI 영향은 `docs/game/03-content-and-ux.md`와 맞춘다.

## Verification

- `.meta`와 serialized YAML 직접 편집은 text serialization, 작은 변경, editor validation 조건을 모두 만족할 때만 한다.
- Missing scripts, missing references, invalid prefab overrides, broken UI route, focus 문제를 확인한다.
- uGUI와 UI Toolkit을 혼용하는 경우 ownership과 event routing을 문서화한다.
- Console errors와 Play Mode/Edit Mode 결과를 최종 응답에 남긴다.
