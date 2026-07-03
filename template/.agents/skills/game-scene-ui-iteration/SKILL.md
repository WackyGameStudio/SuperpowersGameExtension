---
name: game-scene-ui-iteration
description: Use when modifying levels, scenes, maps, actors, GameObjects, prefabs, world objects, spawn points, lighting, collision, navigation, or visual hierarchy in an engine editor.
---

# Game Scene UI Iteration

## Overview

Scene, level, prefab, actor, GameObject, widget, canvas, UIDocument, HUD, menu 변경은 코드 리뷰만으로 충분히 검증되지 않는다. 변경 전후의 구조와 시각 결과를 확인한다.

## Workflow

1. 대상 scene, level, prefab, widget, UI document를 명확히 식별한다.
2. 현재 hierarchy, owner, route, input mode, focus behavior를 snapshot한다.
3. 기대되는 visual result와 player-facing behavior를 한 문단으로 적는다.
4. 가능한 경우 duplicate scene, level, prefab에서 실험한다.
5. Engine editor surface나 MCP를 사용해 작은 단위로 수정한다.
6. 변경 후 hierarchy snapshot, screenshot, console/log, scene validation 중 가능한 검증을 수행한다.
7. `docs/game/03-content-and-ux.md` 갱신 여부를 판단한다.
8. Unity scene/UI snapshot은 `.codex/skills/unity-mcp-skill/SKILL.md`의 `unity-mcp-orchestrator`가 정의한 resource-first 흐름으로 확보한다. 구체적인 MCPForUnity resource/tool 선택과 수집 순서는 local skill pack에 위임한다.
9. HUD/menu/widget/canvas/UIDocument 변경이 visual hierarchy 이상으로 runtime binding, focus/navigation, input mode, screen flow를 바꾸면 `game-ui-implementation`을 함께 사용한다.

## Verification

- Missing reference, missing script, broken widget binding, invalid route, focus loss를 확인한다.
- UI 작업은 keyboard/gamepad/mouse input mode와 safe area를 확인한다.
- Scene 작업은 camera, lighting, collision, navigation, spawn point 같은 runtime-critical object를 확인한다.
- 시각 검증이 불가능하면 구조적 검증과 그 한계를 최종 응답에 남긴다.
