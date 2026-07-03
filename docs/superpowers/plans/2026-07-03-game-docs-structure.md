# Game Docs Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `superpowers-game-extension`의 기본 game docs payload를 compact 구조로 줄이고, `AGENTS.md`, local game skills, README, INSTALL 문서를 같은 정책으로 정렬한다.

**Architecture:** 설치 payload의 source of truth는 `template/` 아래에 유지한다. `template/docs/game/`는 6개 core docs와 2개 로그로 축소하고, `template/AGENTS.md`와 `.agents/skills`는 같은 split criteria와 routing 용어를 공유한다. README와 INSTALL 문서는 template 구조를 설명만 하며, 기존 설치 대상 프로젝트 migration을 자동 수행하지 않는다.

**Tech Stack:** Markdown, PowerShell, Git, `rg`, Codex local skills, Superpowers workflow.

## Global Constraints

- `template/`가 설치 payload의 source of truth이다.
- Extension repo root에는 `.agents/`와 `AGENTS.md`를 만들지 않는다.
- 기존 설치 대상 게임 프로젝트의 old docs를 자동 migration하거나 삭제하지 않는다.
- `game-online-liveops` skill은 이번 기본 payload에 추가하지 않는다.
- Unity/Unreal MCP 자체 설치 절차는 바꾸지 않는다.
- `README.md`와 `README.en.md` 초반에 이미 있는 `Superpowers` 링크 및 설명 문장을 보존한다.
- `docs/game` 기본 파일은 `00-index.md`, `01-product-brief.md`, `02-gameplay-design.md`, `03-content-and-ux.md`, `04-engine-architecture.md`, `05-validation-release.md`, `decision-log.md`, `change-log.md`만 둔다.
- 새 `docs/game` 하위 문서는 split criteria를 만족할 때만 만든다.
- 모든 Markdown 템플릿은 실제 줄바꿈, 명확한 heading, renderable table/code block을 가져야 한다.
- 구현 전 현재 작업 트리에 `README.md`와 `README.en.md`의 기존 미커밋 변경이 있음을 확인하고, 그 변경을 지우지 않는다.

---

## Scope Check

이 spec은 docs template 구조, agent instruction routing, local skill prompt, public install documentation을 함께 바꾸지만 모두 같은 설치 payload 정책을 향한다. 독립 제품 기능이 아니라 하나의 extension template 정렬 작업이므로 단일 구현 계획으로 처리한다.

## File Structure

- `template/docs/game/00-index.md`: core docs map, `docs_profile`, optional expansion map, split criteria, latest validation pointer.
- `template/docs/game/01-product-brief.md`: pitch, target player experience, pillars, audience/platforms, scope, milestone, risks, core loop summary.
- `template/docs/game/02-gameplay-design.md`: loop details, player verbs, input/camera, systems, progression/economy, AI, multiplayer summary, validation path.
- `template/docs/game/03-content-and-ux.md`: scenes/levels, transitions, runtime objects, UI flow, input focus, content/assets, localization/accessibility, reference integrity.
- `template/docs/game/04-engine-architecture.md`: engine identity, runtime modules, editor tools, integration points, data ownership, save/network summaries, source control policy.
- `template/docs/game/05-validation-release.md`: smoke tests, bug reproduction, evidence ledger, performance budgets, profiling path, build/release targets, release blockers.
- `template/docs/game/decision-log.md`: durable decisions and trade-offs.
- `template/docs/game/change-log.md`: player-facing or spec-level changes only.
- `template/AGENTS.md`: game project identification, compact docs policy, skill routing.
- `template/.agents/skills/game-docs-maintaining/SKILL.md`: docs ownership, split criteria, no-op reason, verification workflow.
- `template/.agents/skills/game-build-release-platforms/SKILL.md`: new build/release/platform skill.
- `template/.agents/skills/game-scene-ui-iteration/SKILL.md`: scene/world hierarchy trigger wording.
- `template/.agents/skills/game-ui-implementation/SKILL.md`: runtime UI trigger wording.
- `template/.agents/skills/game-asset-pipeline/SKILL.md`: asset import/taxonomy/reference trigger wording.
- `template/.agents/skills/game-content-branching-and-merging/SKILL.md`: conflict/lock/branching trigger wording.
- `README.md`: Korean public docs, living docs map, skill table.
- `README.en.md`: English public docs, living docs map, skill table.
- `INSTALL_FOR_AI.md`: non-destructive install rules and expected new payload shape.

---

### Task 0: Normalize Markdown Formatting Before Structural Edits

**Files:**
- Inspect: `template/docs/game/*.md`
- Inspect: `template/.agents/skills/*/SKILL.md`
- Inspect: `README.md`
- Inspect: `README.en.md`
- Inspect: `INSTALL_FOR_AI.md`
- Inspect: `template/AGENTS.md`

**Interfaces:**
- Consumes: Current repository state before structural edits.
- Produces: A clean Markdown baseline so later patches operate on renderable headings, paragraphs, tables, and code blocks.

- [ ] **Step 1: Check Markdown line counts**

Run:

```powershell
Get-ChildItem 'template/docs/game/*.md','template/.agents/skills/*/SKILL.md','README.md','README.en.md','INSTALL_FOR_AI.md','template/AGENTS.md' | ForEach-Object {
  $lineCount = (Get-Content -LiteralPath $_.FullName).Count
  if ($lineCount -lt 5) {
    "$($_.FullName) has only $lineCount lines"
  }
}
```

Expected on a clean target: no output.

If output exists, reformat the listed Markdown files into real headings, paragraphs, lists, tables, and code blocks before Task 1. Keep this as a formatting-only change.

- [ ] **Step 2: Commit formatting-only normalization if needed**

Run only if Step 1 found files to normalize:

```powershell
git add template/docs/game template/.agents/skills README.md README.en.md INSTALL_FOR_AI.md template/AGENTS.md
git commit -m "chore: normalize markdown template formatting"
```

Expected: commit succeeds only if formatting normalization was needed. If no files changed, skip this commit.

---

### Task 1: Rebuild `docs/game` Core Templates

**Files:**
- Modify: `template/docs/game/00-index.md`
- Create: `template/docs/game/01-product-brief.md`
- Create: `template/docs/game/02-gameplay-design.md`
- Create: `template/docs/game/03-content-and-ux.md`
- Create: `template/docs/game/04-engine-architecture.md`
- Create: `template/docs/game/05-validation-release.md`
- Modify: `template/docs/game/decision-log.md`
- Modify: `template/docs/game/change-log.md`
- Remove: `template/docs/game/01-vision-and-pillars.md`
- Remove: `template/docs/game/02-core-loop.md`
- Remove: `template/docs/game/03-player-and-controls.md`
- Remove: `template/docs/game/04-gameplay-systems.md`
- Remove: `template/docs/game/05-scenes-and-levels.md`
- Remove: `template/docs/game/06-ui-ux-flow.md`
- Remove: `template/docs/game/07-content-and-assets.md`
- Remove: `template/docs/game/08-technical-architecture.md`
- Remove: `template/docs/game/09-data-and-save-model.md`
- Remove: `template/docs/game/10-playtest-and-qa.md`
- Remove: `template/docs/game/11-performance-budgets.md`
- Remove: `template/docs/game/12-build-release-platforms.md`

**Interfaces:**
- Consumes: Approved spec at `docs/superpowers/specs/2026-07-03-game-docs-structure-design.md`.
- Produces: The canonical 8-file `docs/game` template map that later tasks reference in `AGENTS.md`, skills, README, and INSTALL.

- [ ] **Step 1: Run the pre-change structure check and confirm it fails**

Run:

```powershell
$expected = @(
  '00-index.md',
  '01-product-brief.md',
  '02-gameplay-design.md',
  '03-content-and-ux.md',
  '04-engine-architecture.md',
  '05-validation-release.md',
  'decision-log.md',
  'change-log.md'
)
$actual = Get-ChildItem 'template/docs/game' -File | Sort-Object Name | Select-Object -ExpandProperty Name
Compare-Object $expected $actual
```

Expected on the current old template: output includes old files such as `01-vision-and-pillars.md` or `12-build-release-platforms.md`, and missing new files such as `01-product-brief.md`.

If the check already passes, inspect `git status --short` and continue only after confirming this task was already applied.

- [ ] **Step 2: Replace `template/docs/game/00-index.md` with the compact index**

Use `apply_patch` to replace the full file with:

````md
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
````

- [ ] **Step 3: Create `template/docs/game/01-product-brief.md`**

Use `apply_patch` to add this full file:

```md
# Product Brief

## One-line pitch

아직 기록되지 않음.

## Target player experience

- Intended emotion: 아직 기록되지 않음
- Target audience: 아직 기록되지 않음
- Target platforms: 아직 기록되지 않음

## Design pillars

| Pillar | Meaning | Design pressure |
|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Scope

### In scope

- 아직 기록되지 않음

### Non-goals

- 아직 기록되지 않음

## Current milestone

- Milestone name: 아직 기록되지 않음
- Player-facing goal: 아직 기록되지 않음
- Completion signal: 아직 기록되지 않음

## Core loop summary

아직 기록되지 않음.

## Risks, assumptions, open questions

| Type | Item | Owner | Current response |
|---|---|---|---|
| Risk | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |
```

- [ ] **Step 4: Create `template/docs/game/02-gameplay-design.md`**

Use `apply_patch` to add this full file:

```md
# Gameplay Design

## Core, session, and reward loops

| Loop | Current contract | Validation path |
|---|---|---|
| Core loop | 아직 기록되지 않음 | 아직 기록되지 않음 |
| Session loop | 아직 기록되지 않음 | 아직 기록되지 않음 |
| Reward loop | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Player verbs

| Verb | Input or trigger | Game response | Notes |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Input and camera

- Input system: 아직 기록되지 않음
- Camera states: 아직 기록되지 않음
- Accessibility constraints: 아직 기록되지 않음

## Gameplay systems

| System | Responsibility | Source of truth | Validation path |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Progression and economy

아직 기록되지 않음.

## AI and enemy behavior

아직 기록되지 않음.

## Multiplayer and authority

아직 기록되지 않음.

## Split notes

Combat, AI, progression, economy, or multiplayer details move to `systems/` or `online/` only when the split criteria in `00-index.md` are met.
```

- [ ] **Step 5: Create `template/docs/game/03-content-and-ux.md`**

Use `apply_patch` to add this full file:

```md
# Content and UX

## Scenes, levels, and maps

| Scene or level | Purpose | Entry point | Exit path | Validation path |
|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Scene transition map

아직 기록되지 않음.

## Runtime objects and content taxonomy

| Type | Naming or folder policy | Source or generated | Reference integrity notes |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## UI and UX flow

| Screen or state | Owner | Opens from | Closes to | Focus/navigation notes |
|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Input focus and navigation

아직 기록되지 않음.

## Localization and accessibility

- Localization constraints: 아직 기록되지 않음
- Font/subtitle/readability constraints: 아직 기록되지 않음
- Safe area/platform accessibility constraints: 아직 기록되지 않음

## Split notes

Scene, UI, asset, localization, or accessibility details move to `content/` or `ux/` only when the split criteria in `00-index.md` are met.
```

- [ ] **Step 6: Create `template/docs/game/04-engine-architecture.md`**

Use `apply_patch` to add this full file:

```md
# Engine Architecture

## Engine identity

- Engine: 아직 감지되지 않음
- Engine version: 아직 기록되지 않음
- Primary project file: 아직 기록되지 않음

## Runtime modules and plugins

| Module or plugin | Responsibility | Depends on | Notes |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Editor tools and integration points

| Tool or integration | Purpose | Mutating actions allowed | Verification path |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Data ownership boundaries

아직 기록되지 않음.

## Save schema and migration policy

- Current save schema: 아직 기록되지 않음
- Backward compatibility contract: 아직 기록되지 않음
- Migration validation path: 아직 기록되지 않음

## Networking authority summary

아직 기록되지 않음.

## Engine-owned asset source control policy

- Unity `.meta` files: version control에 포함
- Unity scene/prefab/asset edits: 가능하면 Unity Editor API 또는 MCP를 사용
- Unreal `.uasset` and `.umap` edits: Unreal Editor, MCP, commandlets, 또는 문서화된 engine tooling 사용
- Unreal OFPA/external actor files: Editor/source control integration에서 변경 목록을 검증하고 submit 전에 level/actor reference 상태를 확인
- Generated files: source/generated policy가 기록될 때까지 commit 전에 검토

## Split notes

Runtime modules, save data, online authority, backend/live ops, or editor tooling details move to `architecture/` or `online/` only when the split criteria in `00-index.md` are met.
```

- [ ] **Step 7: Create `template/docs/game/05-validation-release.md`**

Use `apply_patch` to add this full file:

````md
# Validation and Release

## Smoke test matrix

| Area | Scenario | Command or manual path | Expected result | Last evidence |
|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Bug reproduction format

Use this format when adding reproduction evidence:

```text
Build or commit:
Platform:
Steps:
Expected:
Actual:
Evidence:
```

## Validation evidence ledger

| Date | Build or commit | Evidence | Result | Notes |
|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Performance budgets

| Platform | Frame time or FPS | Memory | Loading | Build size | Measurement path |
|---|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Build and release targets

| Target | Version/build number | Build scenes/maps/content | Packaging path | Release checklist | Current blockers |
|---|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Split notes

QA, performance, automation, build, certification, or platform-specific release details move to `validation/` or `platform/` only when the split criteria in `00-index.md` are met.
````

- [ ] **Step 8: Replace `template/docs/game/decision-log.md`**

Use `apply_patch` to replace the full file with:

```md
# Decision Log

Record durable game, technical, content, platform, save, networking, performance, and validation decisions that are costly to reverse or likely to be debated again.

## Entries

| Date | Decision | Options considered | Reason | Impact | Linked evidence |
|---|---|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Recording criteria

Add an entry when a decision changes player-facing behavior, save/network/platform compatibility, performance budget, content production policy, or a trade-off the team is likely to revisit.
```

- [ ] **Step 9: Replace `template/docs/game/change-log.md`**

Use `apply_patch` to replace the full file with:

```md
# Change Log

Record player-facing or spec-level game changes. Do not record internal refactors, file moves, formatting-only edits, or implementation details that do not change the game contract.

## Entries

| Date | Change | Player or spec impact | Validation evidence |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Recording criteria

Add an entry for gameplay behavior changes, content/spec-level changes, save/network/platform compatibility changes, and changes linked to validation evidence.
```

- [ ] **Step 10: Remove obsolete docs**

Run:

```powershell
git rm `
  'template/docs/game/01-vision-and-pillars.md' `
  'template/docs/game/02-core-loop.md' `
  'template/docs/game/03-player-and-controls.md' `
  'template/docs/game/04-gameplay-systems.md' `
  'template/docs/game/05-scenes-and-levels.md' `
  'template/docs/game/06-ui-ux-flow.md' `
  'template/docs/game/07-content-and-assets.md' `
  'template/docs/game/08-technical-architecture.md' `
  'template/docs/game/09-data-and-save-model.md' `
  'template/docs/game/10-playtest-and-qa.md' `
  'template/docs/game/11-performance-budgets.md' `
  'template/docs/game/12-build-release-platforms.md'
```

Expected: Git reports each removed file under `rm`.

- [ ] **Step 11: Verify the core docs file list**

Run:

```powershell
$expected = @(
  '00-index.md',
  '01-product-brief.md',
  '02-gameplay-design.md',
  '03-content-and-ux.md',
  '04-engine-architecture.md',
  '05-validation-release.md',
  'change-log.md',
  'decision-log.md'
)
$actual = Get-ChildItem 'template/docs/game' -File | Sort-Object Name | Select-Object -ExpandProperty Name
Compare-Object ($expected | Sort-Object) $actual
```

Expected: no output.

- [ ] **Step 12: Verify obsolete names are gone from core docs**

Run:

```powershell
rg '01-vision-and-pillars|02-core-loop|03-player-and-controls|04-gameplay-systems|05-scenes-and-levels|06-ui-ux-flow|07-content-and-assets|08-technical-architecture|09-data-and-save-model|10-playtest-and-qa|11-performance-budgets|12-build-release-platforms' template/docs/game
```

Expected: no matches.

- [ ] **Step 13: Commit Task 1**

Run:

```powershell
git add template/docs/game
git commit -m "refactor: compact game docs templates"
```

Expected: commit succeeds and includes only `template/docs/game` changes.

---

### Task 2: Compact `template/AGENTS.md` Routing

**Files:**
- Modify: `template/AGENTS.md`

**Interfaces:**
- Consumes: The 8-file docs map produced by Task 1.
- Produces: Routing policy consumed by README/INSTALL wording and by local game skill descriptions.

- [ ] **Step 1: Run the pre-change routing check**

Run:

```powershell
rg '01-vision-and-pillars|12-build-release-platforms|Superpowers 단계별 game skill routing|살아 있는 게임 문서 자동 확인' template/AGENTS.md
```

Expected on the current old template: matches exist in `template/AGENTS.md`.

If the check already has no matches, inspect `git status --short` and continue only after confirming this task was already applied.

- [ ] **Step 2: Replace `template/AGENTS.md` with compact routing**

Use `apply_patch` to replace the full file with:

```md
# AGENTS.md

## 프로젝트 식별

이 저장소는 게임 프로젝트입니다. Global Superpowers workflow는 그대로 적용합니다. 게임 설계, 엔진 콘텐츠, validation, build/release, `docs/game`에 닿는 작업에서는 관련성이 있는 `.agents/skills` local game skill을 사용합니다.

## 엔진 판별

엔진 관련 작업 전에 저장소 증거를 바탕으로 엔진을 식별합니다.

- Unreal: `*.uproject`, `Config/`, `Content/`, `Source/`, `.uplugin`
- Unity: `ProjectSettings/ProjectVersion.txt`, `Assets/`, `Packages/manifest.json`

둘 다 존재하면 파일이나 엔진 상태를 변경하기 전에 어떤 workspace를 수정하는지 먼저 명시합니다.

## 살아 있는 게임 문서 정책

`docs/game/`는 게임 프로젝트의 compact source of truth입니다. 기본 설치 문서는 다음 6개 핵심 문서와 2개 로그입니다.

- `00-index.md`: 문서 맵, 프로젝트 식별, docs profile, 최신 검증 상태
- `01-product-brief.md`: 비전, pillars, scope/non-goals, target player/platform, risks/open questions
- `02-gameplay-design.md`: core/session/reward loop, player verbs, controls/camera, gameplay systems, validation path
- `03-content-and-ux.md`: scenes/levels, UI flow, content/assets, localization/accessibility, reference integrity
- `04-engine-architecture.md`: engine integration, runtime modules, editor tools, data ownership, save/network summary
- `05-validation-release.md`: smoke tests, playtest evidence, performance budgets, build/release targets
- `decision-log.md`: 중요한 결정과 trade-off
- `change-log.md`: player-facing 또는 spec-level 변경만 기록

게임 규칙, UX flow, scene/content, architecture, save/network compatibility, performance budget, build/release target, validation strategy가 바뀌면 같은 작업에서 관련 문서를 갱신하거나 갱신하지 않는 이유를 남깁니다.

새 `docs/game` 파일은 기본적으로 만들지 않습니다. 다음 중 하나가 맞을 때만 `00-index.md`에 등록하고 하위 문서로 분리합니다.

- 기존 섹션이 약 150-200줄 이상으로 커짐
- 별도 owner/reviewer 또는 별도 QA matrix가 있음
- multiplayer/online, save migration, platform release, performance budget처럼 실패 비용이 큼
- PR 충돌이나 반복 논쟁이 잦아 독립 source of truth가 필요함

모든 Markdown 템플릿은 실제 줄바꿈, 명확한 heading, 갱신 기준을 포함해야 합니다. 필요한 경우 문서별 last verified 또는 evidence pointer를 남기고, 프로젝트 전체 최신 검증 상태는 `00-index.md`와 `05-validation-release.md`에서 관리합니다.

## Game skill routing

요청이 game behavior, engine content, validation, build/release, or `docs/game`에 닿으면 관련 local game skill을 사용합니다.

- 문서/설계/source-of-truth 변경: `game-docs-maintaining`
- 엔진 에디터/MCP/engine-owned asset 변경: `game-engine-mcp-operating` + engine workflow
- Unity 작업: `unity-mcp-workflow`; MCPForUnity가 있으면 `.codex/skills/unity-mcp-skill/SKILL.md`의 `unity-mcp-orchestrator` 절차도 확인
- Unreal 작업: `unreal-mcp-workflow`
- scene/level/map/actor/GameObject/prefab/world object/visual hierarchy: `game-scene-ui-iteration`
- HUD/menu/UI screen/modal flow/UI state/runtime binding/focus/navigation/input mode: `game-ui-implementation`
- asset import/naming/folder/source-generated/reference integrity: `game-asset-pipeline`
- verification/playtest/log/test evidence: `game-playtesting-and-validation`
- performance budget/profiling/build size: `game-performance-budgeting`
- build scenes/maps/packaging/platform targets/CI build/release checklist/certification: `game-build-release-platforms`
- save schema/migration/backward compatibility: `game-save-data-migrations`
- input/camera/control accessibility: `game-input-and-camera-design`
- AI behavior/pathfinding/spawn/perception: `game-ai-behavior-debugging`
- multiplayer authority/replication/prediction/rollback: `game-networking-authority`
- binary asset conflicts/locks/source control layout: `game-content-branching-and-merging`
- localization/accessibility/safe area/platform accessibility: `game-localization-accessibility`

Superpowers 단계에서는 같은 원칙을 적용합니다. `brainstorming`과 design/spec에서는 관련 docs와 domain constraints를 설계에 반영합니다. `writing-plans`에서는 docs update, editor/MCP preflight, validation evidence, rollback task를 계획에 포함합니다. implementation과 verification에서는 작업 domain에 맞는 local skill의 workflow와 evidence 기준을 따릅니다.

## 엔진 에셋 안전

바이너리 엔진 에셋은 직접 편집하지 않습니다. Unreal의 `.uasset`과 `.umap`은 editor, MCP, commandlets, 또는 문서화된 engine tooling을 사용합니다. Unity의 `.unity`, `.prefab`, `.asset`, `.meta`는 가능하면 Unity Editor APIs 또는 MCP를 사용합니다. Direct YAML edits는 text serialization이 활성화되어 있고, 변경 범위가 작으며, editor가 결과를 검증할 수 있을 때만 허용합니다.

파괴적인 scene, content, UI 변경 전에는 현재 상태를 snapshot으로 남기고 rollback 방법을 설명하며, 실험에는 복제한 scene, level, prefab을 우선 사용합니다.

## MCP 안전

Unreal MCP와 Unity MCP는 local editor automation 표면입니다. 도구 호출 전에 editor가 실행 중인지, 올바른 project 또는 instance가 활성화되어 있는지, MCP server가 read-only query에 응답하는지 확인합니다.

인증되지 않은 local engine MCP port를 network에 노출하지 않습니다. local MCP endpoint는 localhost 전용으로 취급합니다.

여러 Unity Editor instance가 있으면 수정 전에 활성 instance를 지정합니다. Unreal MCP에서는 중복 tool call을 피하고 editor tool calls를 직렬 작업으로 취급합니다.

Unity 프로젝트에서 MCPForUnity를 설치하고 설정하면 `.codex/skills/unity-mcp-skill/SKILL.md`가 생성되며, 해당 skill의 frontmatter name은 `unity-mcp-orchestrator`입니다. Unity MCP tool/resource 세부 절차는 이 MCPForUnity local skill을 따르고, game extension skills는 게임 문서, scene/UI 안전, 검증 증거를 조율합니다.

## 완료의 의미는 검증됨

파일 편집만으로 완료를 선언하지 않습니다. 완료에는 적절한 compile, editor refresh, scene 검증, test, console/log 확인, 문서 갱신 조합이 필요합니다.
```

- [ ] **Step 3: Verify old routing headings are gone**

Run:

```powershell
rg 'Superpowers 단계별 game skill routing|살아 있는 게임 문서 자동 확인|01-vision-and-pillars|12-build-release-platforms' template/AGENTS.md
```

Expected: no matches.

- [ ] **Step 4: Verify required new routing terms are present**

Run:

```powershell
rg '01-product-brief|05-validation-release|game-build-release-platforms|compact source of truth|Split criteria|split criteria' template/AGENTS.md
```

Expected: matches include `01-product-brief.md`, `05-validation-release.md`, `game-build-release-platforms`, and `compact source of truth`.

- [ ] **Step 5: Commit Task 2**

Run:

```powershell
git add template/AGENTS.md
git commit -m "docs: compact game agent routing"
```

Expected: commit succeeds and includes only `template/AGENTS.md`.

---

### Task 3: Update Game Skills and Add Build/Release Skill

**Files:**
- Modify: `template/.agents/skills/game-docs-maintaining/SKILL.md`
- Create: `template/.agents/skills/game-build-release-platforms/SKILL.md`
- Modify: `template/.agents/skills/game-scene-ui-iteration/SKILL.md`
- Modify: `template/.agents/skills/game-ui-implementation/SKILL.md`
- Modify: `template/.agents/skills/game-asset-pipeline/SKILL.md`
- Modify: `template/.agents/skills/game-content-branching-and-merging/SKILL.md`

**Interfaces:**
- Consumes: The compact docs map from Task 1 and routing terms from Task 2.
- Produces: Local skill prompts and descriptions used by installed game projects.

- [ ] **Step 1: Run the pre-change skill check**

Run:

```powershell
Test-Path 'template/.agents/skills/game-build-release-platforms/SKILL.md'
rg '01-product-brief|Split criteria|game-build-release-platforms|HUDs, menus, UI Toolkit' template/.agents/skills
```

Expected on the current old template: first command prints `False`; `rg` does not find `game-build-release-platforms` and still finds old overlapping descriptions such as `HUDs, menus, UI Toolkit`.

If `game-build-release-platforms` already exists and the old overlapping descriptions are already gone, inspect `git status --short` and continue only after confirming this task was already applied.

- [ ] **Step 2: Replace `game-docs-maintaining/SKILL.md`**

Use `apply_patch` to replace `template/.agents/skills/game-docs-maintaining/SKILL.md` with:

```md
---
name: game-docs-maintaining
description: Use when changing game design, gameplay behavior, content, UI/UX, engine architecture, save/network data, validation, performance, build targets, release constraints, or docs/game files.
---

# Game Docs Maintaining

## Overview

`docs/game/` is the compact source of truth for the game. Keep it accurate, searchable, and small enough to maintain. Prefer updating an existing core document over creating a new document.

## Core documents

Default docs:

- `00-index.md`
- `01-product-brief.md`
- `02-gameplay-design.md`
- `03-content-and-ux.md`
- `04-engine-architecture.md`
- `05-validation-release.md`
- `decision-log.md`
- `change-log.md`

## Workflow

1. Read `docs/game/00-index.md` first.
2. Identify which core document owns the changed game fact.
3. Read only the relevant core document and any expanded doc linked from the index.
4. If code/editor state and docs disagree, report the stale area before changing docs.
5. Update the smallest relevant section.
6. Update `decision-log.md` only for durable trade-offs or decisions likely to be debated again.
7. Update `change-log.md` only for player-facing or spec-level changes.
8. Do not create a new docs file unless the split criteria below are met.
9. If no docs update is needed, record the no-op reason in the final response.

## Split criteria

Create a new `docs/game` file only when at least one is true:

- The section is larger than about 150-200 lines.
- It has a separate owner/reviewer or QA matrix.
- It covers high-risk compatibility: save migration, networking, platform release, live ops, privacy, performance budget.
- It causes repeated PR conflicts or repeated design debates.
- It needs its own validation evidence ledger.

When splitting:

1. Move details to a focused file under `systems/`, `content/`, `ux/`, `architecture/`, `online/`, `validation/`, `platform/`, or `decisions/`.
2. Leave a short summary and link in the core document.
3. Register the new file in `00-index.md`.
4. Preserve old information unless explicitly superseded.

## Verification

- `00-index.md` matches actual docs files.
- Updated docs identify current status, owner if known, and last verified evidence if relevant.
- Markdown uses real line breaks and renderable headings/tables.
- No duplicate source of truth was created.
- Final response says which docs changed or why docs were not changed.
```

- [ ] **Step 3: Add `game-build-release-platforms/SKILL.md`**

Use `apply_patch` to create `template/.agents/skills/game-build-release-platforms/SKILL.md` with:

```md
---
name: game-build-release-platforms
description: Use when changing build scenes/maps, packaging, platform targets, CI build scripts, store submission, release checklist, platform-specific configuration, or certification constraints.
---

# Game Build Release Platforms

## Overview

Build/release work changes how the game is packaged, validated, and delivered. Treat build target, platform constraints, content inclusion, versioning, and release evidence as one surface.

## Workflow

1. Identify target engine, target platform, build configuration, and distribution path.
2. Check build scenes/maps/content inclusion.
3. Check platform-specific input, rendering, save path, networking, localization, accessibility, and performance constraints.
4. Verify whether CI/build scripts, project settings, packaging config, or store metadata changed.
5. Update `docs/game/05-validation-release.md` or an expanded `platform/build-release.md`.

## Verification

- Build command/configuration is recorded.
- Included scenes/maps/content are verified.
- Platform-specific blockers and unverified certification gaps are documented.
- Build output path/version/build number are recorded when available.
- If a build cannot be run, final response states why and what risk remains.
```

- [ ] **Step 4: Update `game-scene-ui-iteration` frontmatter description**

Use `apply_patch` to replace only the `description:` line in `template/.agents/skills/game-scene-ui-iteration/SKILL.md`:

```yaml
description: Use when modifying levels, scenes, maps, actors, GameObjects, prefabs, world objects, spawn points, lighting, collision, navigation, or visual hierarchy in an engine editor.
```

- [ ] **Step 5: Update `game-ui-implementation` frontmatter description**

Use `apply_patch` to replace only the `description:` line in `template/.agents/skills/game-ui-implementation/SKILL.md`:

```yaml
description: Use when changing HUDs, menus, UI screens, modal flow, UI state ownership, runtime UI binding, focus/navigation, input mode, uGUI, UI Toolkit, UMG, or CommonUI.
```

- [ ] **Step 6: Update `game-asset-pipeline` frontmatter description**

Use `apply_patch` to replace only the `description:` line in `template/.agents/skills/game-asset-pipeline/SKILL.md`:

```yaml
description: Use when changing asset import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, naming, folder taxonomy, source/generated policy, or reference integrity.
```

- [ ] **Step 7: Update `game-content-branching-and-merging` frontmatter description**

Use `apply_patch` to replace only the `description:` line in `template/.agents/skills/game-content-branching-and-merging/SKILL.md`:

```yaml
description: Use when resolving engine asset conflicts, binary asset locks, Unity YAML conflicts, prefab or Blueprint merge issues, Unreal OFPA changes, generated file churn, or content branch strategy.
```

- [ ] **Step 8: Verify skill frontmatter names and descriptions**

Run:

```powershell
Select-String -Path 'template/.agents/skills/*/SKILL.md' -Pattern '^name:|^description:' | Sort-Object Path, LineNumber
```

Expected: output includes `name: game-build-release-platforms`; scene/UI/asset/content-branch descriptions match Steps 4-7.

- [ ] **Step 8A: Update old docs references in every game skill body**

Search all skill files, not only frontmatter:

```powershell
rg '01-vision-and-pillars|02-core-loop|03-player-and-controls|04-gameplay-systems|05-scenes-and-levels|06-ui-ux-flow|07-content-and-assets|08-technical-architecture|09-data-and-save-model|10-playtest-and-qa|11-performance-budgets|12-build-release-platforms' template/.agents/skills
```

Replace old docs references with the compact docs map:

- product/vision/core-loop summary -> `docs/game/01-product-brief.md`
- loop/player verbs/input/camera/systems -> `docs/game/02-gameplay-design.md`
- scenes/UI/assets/localization/accessibility -> `docs/game/03-content-and-ux.md`
- architecture/save/network summary -> `docs/game/04-engine-architecture.md`
- playtest/performance/build/release -> `docs/game/05-validation-release.md`

Run the same `rg` command again.

Expected: no matches.

- [ ] **Step 9: Verify docs skill references new core docs**

Run:

```powershell
rg '01-product-brief|02-gameplay-design|03-content-and-ux|04-engine-architecture|05-validation-release|Split criteria|split criteria' template/.agents/skills/game-docs-maintaining/SKILL.md
```

Expected: matches include all five numbered core docs and split criteria text.

- [ ] **Step 10: Commit Task 3**

Run:

```powershell
git add template/.agents/skills
git commit -m "feat: add build release game skill"
```

Expected: commit succeeds and includes skill prompt changes plus the new `game-build-release-platforms` directory.

---

### Task 4: Update README and INSTALL Documentation

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `INSTALL_FOR_AI.md`

**Interfaces:**
- Consumes: Template docs from Task 1, AGENTS routing from Task 2, skill list from Task 3.
- Produces: Public install and usage documentation that matches the payload.

- [ ] **Step 1: Confirm existing README user changes are still present**

Run:

```powershell
rg 'Superpowers\\]\\(https://github.com/obra/superpowers\\)|Superpowers`는 AI coding agent|Superpowers` is a workflow' README.md README.en.md
```

Expected: matches exist in both README files. If these lines are missing, stop and inspect `git diff README.md README.en.md` before editing.

- [ ] **Step 2: Update `README.md` docs payload description**

Use `apply_patch` to replace the `docs/game/` row in the “설치하면 생기는 것” table with:

```md
| `docs/game/` | 작은 프로젝트도 유지할 수 있는 6개 핵심 문서와 2개 로그 중심의 living docs 템플릿입니다. 대규모 프로젝트는 split criteria에 따라 하위 문서로 확장합니다. |
```

- [ ] **Step 3: Replace `README.md` Living Docs section**

Use `apply_patch` to replace the full `## Living Docs` section up to `## 포함된 game skills` with:

```md
## Living Docs

`docs/game`은 사람과 AI가 함께 보는 compact source of truth입니다. 기본 템플릿은 작은 싱글게임도 유지할 수 있도록 6개 핵심 문서와 2개 로그만 생성합니다. 대규모 멀티플레이, 라이브 서비스, 대량 콘텐츠 프로젝트는 `00-index.md`의 split criteria에 따라 하위 문서로 확장합니다.

기본 문서 맵:

- `00-index.md`: 프로젝트 식별, docs profile, 문서 맵, 최신 검증 상태
- `01-product-brief.md`: 한 줄 피치, 목표 경험, pillars, scope/non-goals, target player/platform, risks/open questions
- `02-gameplay-design.md`: core/session/reward loop, player verbs, controls/camera, gameplay systems, validation path
- `03-content-and-ux.md`: scenes/levels, UI flow, content/assets, localization/accessibility, reference integrity
- `04-engine-architecture.md`: runtime modules, editor tools, engine integration, data ownership, save/network summary
- `05-validation-release.md`: smoke tests, playtest evidence, performance budgets, build/release targets
- `decision-log.md`: 중요한 결정과 trade-off
- `change-log.md`: player-facing 또는 spec-level 변경 사항

새 문서는 기본적으로 만들지 않습니다. 섹션이 커지거나, 별도 owner/QA가 있거나, save/network/platform/liveops처럼 실패 비용이 큰 경우에만 `systems/`, `content/`, `ux/`, `architecture/`, `online/`, `validation/`, `platform/`, `decisions/` 아래로 분리합니다.
```

- [ ] **Step 4: Update `README.md` skill table**

Use `apply_patch` to replace or update the table rows under “포함된 game skills” so each of these rows appears exactly once:

```md
| `game-docs-maintaining` | design, gameplay behavior, content, UI/UX, architecture, save/network data, validation, performance, build targets, release constraints, project documentation |
| `game-engine-mcp-operating` | Unreal/Unity MCP connections, editor tools, engine-owned assets, scene inspection, editor state validation |
| `unity-mcp-workflow` | Unity MCP, Unity Editor automation, scenes, GameObjects, prefabs, ScriptableObjects, uGUI, UI Toolkit, Play Mode, Edit Mode tests |
| `unreal-mcp-workflow` | Unreal MCP, Unreal Editor automation, levels, actors, Blueprints, UMG, CommonUI, materials, PIE, Automation tests |
| `game-scene-ui-iteration` | levels, scenes, maps, actors, GameObjects, prefabs, world objects, spawn points, lighting, collision, navigation, visual hierarchy |
| `game-ui-implementation` | HUDs, menus, UI screens, modal flow, UI state ownership, runtime UI binding, focus/navigation, input mode, uGUI, UI Toolkit, UMG, CommonUI |
| `game-asset-pipeline` | asset import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, naming, folder taxonomy, source/generated policy, reference integrity |
| `game-content-branching-and-merging` | engine asset conflicts, binary asset locks, Unity YAML conflicts, prefab/Blueprint merge issues, Unreal OFPA changes, generated file churn, content branch strategy |
| `game-build-release-platforms` | build scenes/maps, packaging, platform targets, CI build scripts, store submission, release checklist, platform-specific configuration, certification constraints |
```

Keep the existing rows for `game-playtesting-and-validation`, `game-performance-budgeting`, `game-save-data-migrations`, `game-input-and-camera-design`, `game-ai-behavior-debugging`, `game-networking-authority`, and `game-localization-accessibility`, unless their order needs to move to keep the table readable.

- [ ] **Step 5: Update `README.en.md` docs payload description**

Use `apply_patch` to replace the `docs/game/` row in the “What gets installed” table with:

```md
| `docs/game/` | Living docs templates centered on 6 core documents and 2 logs, small enough for compact projects and expandable through split criteria. |
```

- [ ] **Step 6: Replace `README.en.md` Living Docs section**

Use `apply_patch` to replace the full `## Living Docs` section up to `## Included game skills` with:

```md
## Living Docs

`docs/game` is a compact source of truth for people and AI agents to share. The default template creates only 6 core documents and 2 logs so small single-player games can keep the docs current. Large multiplayer, live service, or content-heavy projects expand into subdocuments only through the split criteria in `00-index.md`.

Default document map:

- `00-index.md`: project identity, docs profile, document map, latest validation status
- `01-product-brief.md`: one-line pitch, target experience, pillars, scope/non-goals, target player/platform, risks/open questions
- `02-gameplay-design.md`: core/session/reward loop, player verbs, controls/camera, gameplay systems, validation path
- `03-content-and-ux.md`: scenes/levels, UI flow, content/assets, localization/accessibility, reference integrity
- `04-engine-architecture.md`: runtime modules, editor tools, engine integration, data ownership, save/network summary
- `05-validation-release.md`: smoke tests, playtest evidence, performance budgets, build/release targets
- `decision-log.md`: important decisions and trade-offs
- `change-log.md`: player-facing or spec-level changes

Do not create new docs by default. Split into `systems/`, `content/`, `ux/`, `architecture/`, `online/`, `validation/`, `platform/`, or `decisions/` only when a section grows large, has a separate owner/QA path, or covers high-risk save/network/platform/liveops work.
```

- [ ] **Step 7: Update `README.en.md` skill table**

Use `apply_patch` to replace or update the table rows under “Included game skills” so each of these rows appears exactly once:

```md
| `game-docs-maintaining` | design, gameplay behavior, content, UI/UX, architecture, save/network data, validation, performance, build targets, release constraints, project documentation |
| `game-engine-mcp-operating` | Unreal/Unity MCP connections, editor tools, engine-owned assets, scene inspection, editor state validation |
| `unity-mcp-workflow` | Unity MCP, Unity Editor automation, scenes, GameObjects, prefabs, ScriptableObjects, uGUI, UI Toolkit, Play Mode, Edit Mode tests |
| `unreal-mcp-workflow` | Unreal MCP, Unreal Editor automation, levels, actors, Blueprints, UMG, CommonUI, materials, PIE, Automation tests |
| `game-scene-ui-iteration` | levels, scenes, maps, actors, GameObjects, prefabs, world objects, spawn points, lighting, collision, navigation, visual hierarchy |
| `game-ui-implementation` | HUDs, menus, UI screens, modal flow, UI state ownership, runtime UI binding, focus/navigation, input mode, uGUI, UI Toolkit, UMG, CommonUI |
| `game-asset-pipeline` | asset import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, naming, folder taxonomy, source/generated policy, reference integrity |
| `game-content-branching-and-merging` | engine asset conflicts, binary asset locks, Unity YAML conflicts, prefab/Blueprint merge issues, Unreal OFPA changes, generated file churn, content branch strategy |
| `game-build-release-platforms` | build scenes/maps, packaging, platform targets, CI build scripts, store submission, release checklist, platform-specific configuration, certification constraints |
```

Keep the existing rows for `game-playtesting-and-validation`, `game-performance-budgeting`, `game-save-data-migrations`, `game-input-and-camera-design`, `game-ai-behavior-debugging`, `game-networking-authority`, and `game-localization-accessibility`, unless their order needs to move to keep the table readable.

- [ ] **Step 8: Update `INSTALL_FOR_AI.md` source files section**

Use `apply_patch` to add this paragraph after the source tree block:

````md
The expected default `docs/game/` payload is:

```text
docs/game/
  00-index.md
  01-product-brief.md
  02-gameplay-design.md
  03-content-and-ux.md
  04-engine-architecture.md
  05-validation-release.md
  decision-log.md
  change-log.md
```
````

- [ ] **Step 9: Update `INSTALL_FOR_AI.md` docs install rules**

Use `apply_patch` to add this bullet under `### 3. docs/game` rules:

```md
- If the target already has older docs such as `01-vision-and-pillars.md` or `12-build-release-platforms.md`, do not delete or migrate them automatically. Report them as existing project docs and copy only missing current template files.
```

- [ ] **Step 10: Update `INSTALL_FOR_AI.md` verification summary**

Use `apply_patch` to replace:

```md
- `<target-game-project>/docs/game/00-index.md` exists or was reported as already present.
```

with:

```md
- `<target-game-project>/docs/game/00-index.md` and the current core docs exist or were reported as already present.
```

- [ ] **Step 11: Verify old README doc names are gone**

Run:

```powershell
rg '01-vision-and-pillars|02-core-loop|03-player-and-controls|04-gameplay-systems|05-scenes-and-levels|06-ui-ux-flow|07-content-and-assets|08-technical-architecture|09-data-and-save-model|10-playtest-and-qa|11-performance-budgets|12-build-release-platforms' README.md README.en.md
```

Expected: no matches.

- [ ] **Step 12: Verify INSTALL only mentions old names in the non-migration rule**

Run:

```powershell
rg '01-vision-and-pillars|02-core-loop|03-player-and-controls|04-gameplay-systems|05-scenes-and-levels|06-ui-ux-flow|07-content-and-assets|08-technical-architecture|09-data-and-save-model|10-playtest-and-qa|11-performance-budgets|12-build-release-platforms' INSTALL_FOR_AI.md
```

Expected: matches appear only in the rule that says not to delete or migrate older docs automatically. Prefer keeping only 1-2 old doc examples in that rule.

- [ ] **Step 13: Verify README user changes are preserved**

Run:

```powershell
rg 'Superpowers\\]\\(https://github.com/obra/superpowers\\)|Superpowers`는 AI coding agent|Superpowers` is a workflow' README.md README.en.md
```

Expected: matches still exist in both README files.

- [ ] **Step 13A: Verify README skill rows are unique**

Run:

```powershell
$files = @('README.md', 'README.en.md')
$skills = @(
  'game-docs-maintaining',
  'game-engine-mcp-operating',
  'unity-mcp-workflow',
  'unreal-mcp-workflow',
  'game-scene-ui-iteration',
  'game-ui-implementation',
  'game-asset-pipeline',
  'game-content-branching-and-merging',
  'game-build-release-platforms',
  'game-playtesting-and-validation',
  'game-performance-budgeting',
  'game-save-data-migrations',
  'game-input-and-camera-design',
  'game-ai-behavior-debugging',
  'game-networking-authority',
  'game-localization-accessibility'
)
foreach ($file in $files) {
  foreach ($skill in $skills) {
    $count = (Select-String -Path $file -Pattern "\| ``$skill`` \|" -AllMatches).Count
    if ($count -ne 1) { "$file has $count rows for $skill" }
  }
}
```

Expected: no output.

- [ ] **Step 14: Commit Task 4**

Run:

```powershell
git add README.md README.en.md INSTALL_FOR_AI.md
git commit -m "docs: update install docs for compact game docs"
```

Expected: commit succeeds and includes README/INSTALL changes. The existing README user changes are included, not reverted.

---

### Task 5: Final Consistency Verification

**Files:**
- No planned source edits. If a verification failure exposes a mismatch, modify the smallest owning file and rerun the failed check.

**Interfaces:**
- Consumes: Commits from Tasks 0-4.
- Produces: Fresh evidence that the payload, routing, skills, README, and INSTALL are aligned.

- [ ] **Step 1: Verify worktree status before final checks**

Run:

```powershell
git status --short
```

Expected: no output. If output exists, inspect each file and confirm it belongs to a verification fix before continuing.

- [ ] **Step 2: Verify docs template file list exactly**

Run:

```powershell
$expected = @(
  '00-index.md',
  '01-product-brief.md',
  '02-gameplay-design.md',
  '03-content-and-ux.md',
  '04-engine-architecture.md',
  '05-validation-release.md',
  'change-log.md',
  'decision-log.md'
)
$actual = Get-ChildItem 'template/docs/game' -File | Sort-Object Name | Select-Object -ExpandProperty Name
Compare-Object ($expected | Sort-Object) $actual
```

Expected: no output.

- [ ] **Step 3: Verify all current docs are referenced in README, AGENTS, and INSTALL**

Run:

```powershell
$docs = @(
  '00-index.md',
  '01-product-brief.md',
  '02-gameplay-design.md',
  '03-content-and-ux.md',
  '04-engine-architecture.md',
  '05-validation-release.md',
  'decision-log.md',
  'change-log.md'
)
$files = @('README.md', 'README.en.md', 'INSTALL_FOR_AI.md', 'template/AGENTS.md')
foreach ($file in $files) {
  foreach ($doc in $docs) {
    if (-not (Select-String -Path $file -Pattern ([regex]::Escape($doc)) -Quiet)) {
      "$file missing $doc"
    }
  }
}
```

Expected: no output.

- [ ] **Step 4: Verify obsolete docs are not referenced outside intentional migration text and the spec/plan history**

Run:

```powershell
$oldDocs = '01-vision-and-pillars|02-core-loop|03-player-and-controls|04-gameplay-systems|05-scenes-and-levels|06-ui-ux-flow|07-content-and-assets|08-technical-architecture|09-data-and-save-model|10-playtest-and-qa|11-performance-budgets|12-build-release-platforms'
rg $oldDocs README.md README.en.md template
```

Expected: no matches in README or `template/`.

Run:

```powershell
rg $oldDocs INSTALL_FOR_AI.md
```

Expected: matches only in intentional non-migration examples, if any.

- [ ] **Step 5: Verify skill frontmatter includes new skill and updated descriptions**

Run:

```powershell
Select-String -Path 'template/.agents/skills/*/SKILL.md' -Pattern '^name:|^description:' | Sort-Object Path, LineNumber
```

Expected: output includes `name: game-build-release-platforms`; updated descriptions from Task 3 are visible.

- [ ] **Step 6: Verify README skill rows are unique**

Run:

```powershell
$files = @('README.md', 'README.en.md')
$skills = @(
  'game-docs-maintaining',
  'game-engine-mcp-operating',
  'unity-mcp-workflow',
  'unreal-mcp-workflow',
  'game-scene-ui-iteration',
  'game-ui-implementation',
  'game-asset-pipeline',
  'game-content-branching-and-merging',
  'game-build-release-platforms',
  'game-playtesting-and-validation',
  'game-performance-budgeting',
  'game-save-data-migrations',
  'game-input-and-camera-design',
  'game-ai-behavior-debugging',
  'game-networking-authority',
  'game-localization-accessibility'
)
foreach ($file in $files) {
  foreach ($skill in $skills) {
    $count = (Select-String -Path $file -Pattern "\| ``$skill`` \|" -AllMatches).Count
    if ($count -ne 1) { "$file has $count rows for $skill" }
  }
}
```

Expected: no output.

- [ ] **Step 7: Verify Markdown line structure**

Run:

```powershell
Get-ChildItem 'template/docs/game/*.md','template/.agents/skills/*/SKILL.md','README.md','README.en.md','INSTALL_FOR_AI.md','template/AGENTS.md' | ForEach-Object {
  $lineCount = (Get-Content -LiteralPath $_.FullName).Count
  if ($lineCount -lt 5) {
    "$($_.FullName) has only $lineCount lines"
  }
}
```

Expected: no output.

- [ ] **Step 8: Verify docs index does not point to missing files**

Run:

```powershell
$index = Get-Content 'template/docs/game/00-index.md' -Raw
$matches = [regex]::Matches($index, '`([^`]+\.md)`') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
foreach ($match in $matches) {
  $path = Join-Path 'template/docs/game' $match
  if (-not (Test-Path $path)) {
    "Missing linked doc: $match"
  }
}
```

Expected: no output.

- [ ] **Step 9: Verify final git diff is empty**

Run:

```powershell
git status --short
```

Expected: no output.

- [ ] **Step 10: Record verification result in final response**

Final response must include:

```text
Implemented compact docs structure.
Verification run:
- docs file list check
- stale old-doc references check
- skill frontmatter check
- README skill row uniqueness check
- Markdown line structure check
- docs index link check
```

Mention any check that could not be run and the exact remaining risk.

---

## Plan Self-Review Notes

- Spec coverage: Task 0 covers Markdown normalization; Tasks 1-4 map directly to docs template structure, AGENTS routing, skill prompt changes, README/INSTALL updates, and preservation of existing README changes. Task 5 covers the verification strategy from the spec.
- Placeholder scan: The plan has no incomplete task steps or references to undefined files. Template starter content uses `아직 기록되지 않음`, which is intentional installed template text.
- Interface consistency: The produced docs map in Task 1 is consumed by Tasks 2-5. `game-build-release-platforms` is added in Task 3 and referenced by Task 4.
