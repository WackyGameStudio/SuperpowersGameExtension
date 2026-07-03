---
name: game-ui-implementation
description: Use when implementing or changing HUDs, menus, UI Toolkit, uGUI, UMG, CommonUI, UI navigation, focus behavior, or runtime UI binding in a game.
---

# Game UI Implementation

## Overview

HUD, menu, runtime UI binding, focus/navigation, input mode 변경은 player-facing behavior와 gameplay state ownership에 영향을 준다. Scene hierarchy 자체보다 UI architecture와 interaction contract를 확인한다.

## Workflow

1. UI technology surface를 식별한다: Unity uGUI, Unity UI Toolkit, Unreal UMG, Unreal CommonUI, 또는 project-specific UI framework.
2. Screen flow, modal stack, focus/navigation, input mode, safe area, text expansion risk를 정리한다.
3. UI state와 gameplay state의 ownership을 분리해 missing reference, stale data, lifecycle timing risk를 줄인다.
4. UI hierarchy나 scene object 변경이 있으면 `game-scene-ui-iteration`을 함께 사용한다.
5. Localization, font, safe area, readability 영향이 있으면 `game-localization-accessibility`를 함께 사용한다.
6. 변경 후 `docs/game/06-ui-ux-flow.md` 갱신 여부를 판단한다.

## Verification

- UI hierarchy snapshot 또는 screen flow evidence를 남긴다.
- Keyboard, mouse, gamepad/controller navigation 중 target input에 맞는 path를 확인한다.
- Binding, missing reference, focus loss, input mode conflict, localization expansion risk를 확인한다.
- UI-only 변경이라도 console/log check 또는 editor validation이 가능하면 수행한다.
