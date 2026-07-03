---
name: game-docs-maintaining
description: Use when a game task affects design, gameplay rules, scenes, UI flow, content, architecture, save data, testing, performance, build targets, or project documentation.
---

# Game Docs Maintaining

## Overview

게임 프로젝트의 코드, scene, UI, content, validation 상태가 `docs/game/`와 어긋나지 않도록 유지한다.

## Workflow

1. `docs/game/00-index.md`를 먼저 읽는다.
2. 작업 영향 범위에 맞는 `docs/game` 문서를 추가로 읽는다.
3. 현재 코드나 editor 상태가 문서와 다르면 stale 상태를 사용자에게 알린다.
4. 변경 계획이나 구현 결과가 game rules, UX flow, scene structure, architecture, validation strategy에 영향을 주는지 판단한다.
5. 영향이 있으면 관련 문서와 `change-log.md`를 같은 작업에서 갱신한다.
6. 중요한 trade-off가 있으면 `decision-log.md`에 날짜, 결정, 선택지, 이유, 영향을 남긴다.
7. `brainstorming` 중 game design, UI, scene, asset, save, performance, input, AI, networking, accessibility 영향이 있으면 `docs/game/00-index.md`와 관련 docs를 먼저 확인한다.
8. `writing-plans` 중 docs update, `change-log.md`, `decision-log.md` 작업을 계획에 포함한다.
9. `executing-plans` 또는 `subagent-driven-development` 중 game behavior나 engine content 변경 후 docs 갱신 필요 여부를 확인한다.
10. Code review에서는 docs drift, stale index, missing validation evidence, missing change-log를 risk로 본다.
11. `verification-before-completion`에서는 docs updated 또는 no-op reason을 확인한다.
12. `finishing-a-development-branch`에서는 docs map, change-log, decision-log, 신규 docs template 포함 여부를 확인한다.

## Verification

- `docs/game/00-index.md`의 문서 지도가 실제 파일 목록과 맞는지 확인한다.
- 변경된 gameplay, scene, UI, architecture, validation 내용이 관련 문서에 반영됐는지 확인한다.
- Mermaid는 flow, state, transition이 prose보다 명확할 때만 사용한다.
- 문서 갱신이 필요 없다고 판단한 경우, 최종 응답에 그 이유를 짧게 남긴다.
