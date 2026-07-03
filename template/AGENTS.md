# AGENTS.md

<!-- superpowers-game-extension: game-project-instructions -->

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
