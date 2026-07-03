---
name: game-playtesting-and-validation
description: Use when verifying gameplay behavior, reproducing bugs, running Unity Edit or Play Mode tests, Unreal Automation tests, functional tests, smoke tests, or editor log checks.
---

# Game Playtesting and Validation

## Overview

Compile 성공은 game behavior 검증이 아니다. Gameplay, scene, UI, content 변경은 가능한 수준의 automated test, smoke test, editor log check, manual evidence를 남겨야 한다.

## Workflow

1. 검증하려는 behavior나 bug reproduction path를 한 문단으로 정리한다.
2. Unity Edit Mode, Unity Play Mode, Unreal Automation, Unreal Functional Test, smoke test, manual playtest 중 맞는 검증 레벨을 선택한다.
3. 실패를 먼저 재현할 수 있으면 failing validation을 기록한다.
4. 수정 후 같은 path로 passing validation을 기록한다.
5. Command, environment, scene/map, log excerpt, pass/fail을 `docs/game/05-validation-release.md`에 남길지 판단한다.
6. Unity script/test 검증은 `.codex/skills/unity-mcp-skill/SKILL.md`의 `unity-mcp-orchestrator`가 정의한 compile, console, test 확인 순서를 따른다.
7. Performance budget, save migration, networking authority, localization/accessibility처럼 domain-specific evidence가 필요한 작업은 해당 domain skill의 Verification을 함께 적용한다.

## Verification

- UI/scene/content 변경은 console/log check를 포함한다.
- Test가 없으면 최소 smoke validation 절차를 수행하거나, 수행하지 못한 이유를 최종 응답에 남긴다.
- Bug fix는 reproduction path와 fixed evidence를 함께 제시한다.
- Performance나 build target 검증은 이 MVP skill에서 깊게 다루지 않고 후속 `game-performance-budgeting` 대상임을 명시한다.
