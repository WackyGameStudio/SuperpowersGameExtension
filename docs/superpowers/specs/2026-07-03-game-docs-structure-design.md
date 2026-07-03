# 게임 문서 구조 개편 설계

작성일: 2026-07-03
대상 저장소: `superpowers-game-extension`
상태: 사용자 승인 후 recheck 보완 반영

## 배경

현재 extension은 대상 Unity/Unreal 게임 프로젝트에 `AGENTS.md`, `.agents/skills/`, `docs/game/` 템플릿을 설치한다. 기존 `docs/game` 기본 템플릿은 15개 문서로 구성되어 있어 대규모 게임 프로젝트의 주제는 넓게 포착하지만, 소규모 게임이나 prototype에는 빈 문서와 갱신 부담을 많이 만든다.

외부 분석 문서는 기본 설치 문서를 6개 핵심 문서와 2개 로그로 줄이고, 대형 프로젝트는 split criteria를 만족할 때만 하위 문서로 확장하는 방향을 권장했다. 현재 workspace 확인 결과 `template/docs/game/*.md`와 `template/.agents/skills/*/SKILL.md`는 이미 실제 줄바꿈을 가진 Markdown 파일이다. 다만 branch나 원격 raw 상태 차이를 방어하기 위해 구현 계획에는 구조 변경 전 Markdown line structure normalization 확인을 별도 Task 0으로 둔다.

## 목표

- 기본 `docs/game` 설치 payload를 작고 유지 가능한 compact source of truth로 만든다.
- 문서 구조, `AGENTS.md`, skill prompt, README, INSTALL 설명이 같은 정책을 가리키게 한다.
- agent가 작은 작업에서 새 문서를 과생성하지 않도록 split criteria를 명확히 한다.
- build/release/platform 변경을 직접 다루는 local skill을 추가한다.
- 기존 사용자 변경인 `README.md`와 `README.en.md` 초반의 `Superpowers` 링크 및 설명 문장을 보존한다.

## 비목표

- 기존 설치 대상 게임 프로젝트의 old docs를 자동 migration하거나 삭제하지 않는다.
- `game-online-liveops` 같은 대규모 live service 전용 skill은 이번 기본 payload에 추가하지 않는다.
- Unity/Unreal MCP 자체 설치 절차를 바꾸지 않는다.
- extension repo root에 `.agents/`나 `AGENTS.md`를 만들지 않는다.

## 선택한 접근

선택한 접근은 “구조 개편 + routing 정리 + build/release skill 추가”이다.

대안 A는 문서 구조만 축소하는 방식이었다. 빠르지만 `AGENTS.md`와 skill prompt가 이전 구조를 계속 유도해 문서 과생성 문제가 남는다.

대안 B는 `docs/game`, `AGENTS.md`, `game-docs-maintaining`, 겹치는 skill descriptions, README/INSTALL을 같은 정책으로 정렬한다. 일관성과 유지보수성이 가장 좋으므로 이 방식을 채택한다.

대안 C는 B에 pressure scenario 테스트 문서까지 추가하는 방식이었다. 검증력은 높지만 기본 설치 payload가 무거워지므로, 이번에는 README/skill의 규칙과 수동 검증으로 충분하다고 판단한다.

## Docs 템플릿 구조

`template/docs/game/` 기본 파일은 다음 8개로 줄인다.

```text
00-index.md
01-product-brief.md
02-gameplay-design.md
03-content-and-ux.md
04-engine-architecture.md
05-validation-release.md
decision-log.md
change-log.md
```

기존 문서의 정보는 다음 기준으로 병합한다.

| 기존 파일 | 새 위치 |
|---|---|
| `01-vision-and-pillars.md` | `01-product-brief.md` |
| `02-core-loop.md` | `01-product-brief.md` 요약, `02-gameplay-design.md` 상세 |
| `03-player-and-controls.md` | `02-gameplay-design.md` |
| `04-gameplay-systems.md` | `02-gameplay-design.md` |
| `05-scenes-and-levels.md` | `03-content-and-ux.md` |
| `06-ui-ux-flow.md` | `03-content-and-ux.md` |
| `07-content-and-assets.md` | `03-content-and-ux.md` |
| `08-technical-architecture.md` | `04-engine-architecture.md` |
| `09-data-and-save-model.md` | `04-engine-architecture.md` |
| `10-playtest-and-qa.md` | `05-validation-release.md` |
| `11-performance-budgets.md` | `05-validation-release.md` |
| `12-build-release-platforms.md` | `05-validation-release.md` |
| `decision-log.md` | 유지 |
| `change-log.md` | 유지하되 player-facing 또는 spec-level 변경만 기록 |

`00-index.md`는 다음을 포함한다.

- 게임 제목, 엔진, 주요 플랫폼, 현재 마일스톤
- `docs_profile`: `compact`, `standard`, `expanded`
- 핵심 문서 맵
- optional expansion directories
- latest validation evidence pointer
- split criteria

`docs_profile` 값은 `00-index.md` 안에서 다음 의미를 설명한다.

- `compact`: prototype 또는 소규모 solo/single-player 프로젝트. 하위 문서를 만들지 않고 core docs만 유지한다.
- `standard`: 기본값. 6개 핵심 문서와 2개 로그를 유지하고 split criteria를 만족할 때만 분리한다.
- `expanded`: 대규모 multiplayer, live service, 대량 content, 또는 platform-heavy 프로젝트. `00-index.md`에 등록된 하위 문서를 함께 유지한다.

새 하위 문서는 기본 생성하지 않는다. 다음 중 하나가 맞을 때만 `systems/`, `content/`, `ux/`, `architecture/`, `online/`, `validation/`, `platform/`, `decisions/` 아래로 분리한다.

- 기존 섹션이 약 150-200줄 이상으로 커짐
- 별도 owner/reviewer 또는 별도 QA matrix가 있음
- save migration, networking, platform release, live ops, privacy, performance budget처럼 실패 비용이 큼
- PR 충돌이나 반복 논쟁이 잦음
- 별도 validation evidence ledger가 필요함

## AGENTS.md 설계

`template/AGENTS.md`는 세 역할에 집중한다.

- 저장소 증거 기반 Unity/Unreal 엔진 판별
- `docs/game/` compact source of truth 정책
- 작업 종류별 local game skill trigger

Living docs 정책은 새 8개 문서 기준으로 짧게 정리한다. 핵심 규칙은 게임 규칙, UX flow, scene/content, architecture, save/network compatibility, performance budget, build/release target, validation strategy가 바뀌면 같은 작업에서 관련 문서를 갱신하거나 갱신하지 않는 이유를 남기는 것이다.

Evidence 정책은 모든 문서에 같은 섹션을 강제하지 않는다. 필요한 경우 각 문서에 last verified 또는 evidence pointer를 포함하고, 프로젝트 전체 최신 검증 상태는 `00-index.md`와 `05-validation-release.md`에서 관리한다.

긴 단계별 조합 표는 줄이고, `Superpowers` stage마다 관련 domain skill을 적용한다는 원칙만 유지한다. 세부 workflow와 verification은 개별 `SKILL.md`가 책임진다.

## Skill prompt 설계

`game-docs-maintaining`은 새 문서 구조의 중심 규칙으로 바꾼다.

- `docs/game/00-index.md`를 먼저 읽는다.
- 변경된 game fact를 소유하는 core document를 찾는다.
- 관련 core document와 index에 연결된 expanded doc만 읽는다.
- 가장 작은 관련 section을 갱신한다.
- split criteria를 만족하지 않으면 새 `docs/game` 파일을 만들지 않는다.
- `decision-log.md`는 durable trade-off 또는 반복 논쟁 가능성이 큰 결정에만 갱신한다.
- `change-log.md`는 player-facing 또는 spec-level 변경에만 갱신한다.
- 문서 갱신이 필요 없으면 최종 응답에 no-op reason을 남긴다.

새 skill `game-build-release-platforms`를 추가한다. 적용 대상은 build scenes/maps, packaging, platform targets, CI build scripts, store submission, release checklist, platform-specific configuration, certification constraints이다.

겹치는 skill descriptions는 다음처럼 분리한다.

- `game-scene-ui-iteration`: level, scene, map, actor, GameObject, prefab, world object, spawn point, lighting, collision, navigation, visual hierarchy 중심
- `game-ui-implementation`: HUD, menu, UI screen, modal flow, UI state ownership, runtime UI binding, focus/navigation, input mode, uGUI, UI Toolkit, UMG, CommonUI 중심
- `game-asset-pipeline`: import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, naming, folder taxonomy, source/generated policy, reference integrity 중심
- `game-content-branching-and-merging`: engine asset conflicts, binary asset locks, Unity YAML conflicts, prefab/Blueprint merge issues, Unreal OFPA changes, generated file churn, content branch strategy 중심

Frontmatter뿐 아니라 모든 game skill 본문에서 old docs 참조를 새 core docs 참조로 교체한다.

- product/vision/core-loop summary -> `docs/game/01-product-brief.md`
- loop/player verbs/input/camera/systems -> `docs/game/02-gameplay-design.md`
- scenes/UI/assets/localization/accessibility -> `docs/game/03-content-and-ux.md`
- architecture/save/network summary -> `docs/game/04-engine-architecture.md`
- playtest/performance/build/release -> `docs/game/05-validation-release.md`

기존 다른 game skills는 유지한다.

## README와 INSTALL 설계

`README.md`와 `README.en.md`는 같은 의미로 갱신한다. Living Docs 섹션은 6개 핵심 문서와 2개 로그, 조건부 확장 구조를 설명한다. Included game skills 표에는 `game-build-release-platforms`를 추가하고, 겹침을 줄인 skill 설명을 반영한다.

`INSTALL_FOR_AI.md`의 비파괴 설치 원칙은 유지한다.

- `AGENTS.md`는 기존 규칙대로 create/replace-empty/append-only를 따른다.
- `.agents/skills/`는 누락된 skill directory만 복사하고 기존 directory는 conflict로 보고한다.
- `docs/game/`는 누락된 template file만 복사하고 기존 파일은 덮어쓰지 않는다.
- 기존 대상 프로젝트에 old docs가 있어도 삭제하지 않고 already present 또는 conflict로 보고한다.

## 검증 전략

구현 후 다음을 확인한다.

- `template/docs/game` 실제 파일 목록이 `00-index.md`, README, INSTALL 설명과 일치한다.
- `README.md`, `README.en.md`, `template/`, `template/.agents/skills`에는 old docs 파일명 참조가 남아 있지 않다.
- `INSTALL_FOR_AI.md`의 old docs 참조는 자동 migration 금지 예시로만 남는다.
- skill frontmatter의 `name`과 `description`이 새 routing과 맞는다.
- skill 본문 docs 참조가 새 core docs map과 맞는다.
- Markdown heading, table, code block이 실제 줄바꿈을 가진다.
- `README.md`와 `README.en.md` 초반의 기존 사용자 변경이 보존됐다.
- `game-build-release-platforms/SKILL.md`가 포함된 skill 목록과 README 표가 일치한다.
- README/README.en skill table에는 각 skill row가 정확히 한 번씩만 등장한다.
- `00-index.md`의 Markdown 링크가 실제 docs 파일을 가리킨다.

## 구현 순서

0. 구조 변경 전 Markdown line structure를 확인하고, one-line Markdown 파일이 있으면 formatting-only normalization을 별도 commit으로 처리한다.
1. `template/docs/game`를 8개 core docs로 재구성한다.
2. `template/AGENTS.md`를 compact policy와 trigger 중심으로 정리한다.
3. `game-docs-maintaining`과 겹치는 skill descriptions를 갱신하고 `game-build-release-platforms`를 추가한다.
4. 모든 game skill 본문에서 old docs 참조를 새 core docs 참조로 교체한다.
5. `README.md`, `README.en.md`, `INSTALL_FOR_AI.md`를 새 구조에 맞춘다.
6. 파일 목록, stale references, skill frontmatter/body, Markdown 구조, README skill 중복, docs index link를 검증한다.

## 위험과 대응

- 기존 파일 삭제로 인해 설치 대상 migration처럼 보일 수 있다. 이번 변경은 extension template만 바꾸며, `INSTALL_FOR_AI.md`는 기존 대상 프로젝트 파일을 삭제하지 않는다고 명시한다.
- README와 template이 서로 다른 문서 맵을 가리킬 수 있다. 구현 검증에서 `rg`와 파일 목록 비교로 stale reference를 확인한다.
- build/release skill 추가로 기본 skill pack이 커질 수 있다. 하지만 기존 문서에 build/release가 이미 있었고 직접 대응 skill이 없었으므로, 기본 payload에 포함하는 편이 더 일관적이다.
- `game-scene-ui-iteration`과 `game-ui-implementation`은 여전히 일부 작업에서 함께 필요할 수 있다. description은 trigger 중심을 분리하되, 실제 routing은 필요 시 함께 사용할 수 있게 둔다.
- 구현 계획의 Markdown snippet 안에 nested code fence가 들어갈 수 있다. plan 문서 자체 렌더링이 깨지지 않도록 nested fence가 필요한 snippet은 4-backtick fence를 사용한다.

## 검토 기록

사용자는 2026-07-03에 다음 설계 섹션을 순차 승인했다.

- 전체 범위와 산출물
- Docs 템플릿 구조
- `AGENTS.md`와 skill routing
- Skill prompt 변경
- README, INSTALL, 검증 전략

2026-07-03 recheck 문서를 기준으로 다음 보완을 반영했다.

- 구현 계획의 nested Markdown code fence 방지
- 구현 전 Markdown line structure normalization Task 0 추가
- 모든 game skill 본문 old docs 참조 제거 요구
- evidence 정책을 `00-index.md`와 `05-validation-release.md` 중심으로 완화
- README skill row 중복 검증 및 INSTALL old-doc 검사 범위 확장
