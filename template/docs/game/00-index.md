# 게임 문서 색인

## 프로젝트 식별

- 게임 제목: 아직 기록되지 않음
- 엔진: 아직 감지되지 않음
- 주요 플랫폼: 아직 기록되지 않음
- 현재 마일스톤: 아직 기록되지 않음
- docs_profile: `standard`

## 핵심 문서 맵

`docs/game/`는 사람과 AI agent가 함께 보는 compact source of truth입니다. 기본 설치 문서는 6개 핵심 문서와 2개 로그만 유지합니다.

- `01-product-brief.md`: 비전, pillars, scope/non-goals, target player/platform, risks/open questions, core loop 요약
- `02-gameplay-design.md`: core/session/reward loop, player verbs, controls/camera, gameplay systems, validation path
- `03-content-and-ux.md`: scenes/levels, UI flow, content/assets, localization/accessibility, reference integrity
- `04-engine-architecture.md`: engine integration, runtime modules, editor tools, data ownership, save/network summary
- `05-validation-release.md`: smoke tests, playtest evidence, performance budgets, build/release targets
- `decision-log.md`: 중요한 결정과 trade-off
- `change-log.md`: player-facing 또는 spec-level 변경

## Docs profile

- `compact`: prototype 또는 소규모 solo/single-player 프로젝트. 하위 문서를 만들지 않고 core docs만 유지합니다.
- `standard`: 기본값. 6개 핵심 문서와 2개 로그를 유지하고 split criteria를 만족할 때만 분리합니다.
- `expanded`: 대규모 multiplayer, live service, 대량 content, 또는 platform-heavy 프로젝트. `00-index.md`에 등록된 하위 문서를 함께 유지합니다.

## Optional expansion directories

새 문서는 기본적으로 만들지 않습니다. 아래 디렉터리는 split criteria를 만족할 때만 생성하고 이 색인에 등록합니다.

```text
systems/
content/
ux/
architecture/
online/
validation/
platform/
decisions/
```

## Split criteria

다음 중 하나 이상이 맞을 때만 핵심 문서의 세부 내용을 하위 문서로 분리합니다.

- 기존 섹션이 약 150-200줄 이상으로 커짐
- 별도 owner/reviewer 또는 별도 QA matrix가 있음
- save migration, networking, platform release, live ops, privacy, performance budget처럼 실패 비용이 큼
- PR 충돌이나 반복 논쟁이 잦음
- 별도 validation evidence ledger가 필요함

분리할 때는 핵심 문서에 짧은 요약과 링크를 남기고, 새 파일을 이 색인에 등록합니다.

## 최신 검증 상태

- Last verified: 아직 검증 증거가 기록되지 않음
- Evidence pointer: 아직 기록되지 않음

## 유지보수 원칙

게임 규칙, UX flow, scene/content, architecture, save/network compatibility, performance budget, build/release target, validation strategy가 바뀌면 같은 작업에서 관련 문서를 갱신하거나 갱신하지 않는 이유를 남깁니다.
