# AGENTS.md

## 프로젝트 식별

이 저장소는 게임 프로젝트입니다. Global Superpowers 워크플로는 그대로 적용됩니다. 추가로 게임 엔진 관련 작업에서는 관련성이 있을 때 `.agents/skills` 안의 로컬 game skills를 사용해야 합니다.

## 엔진 판별

엔진 관련 작업 전에 저장소 증거를 바탕으로 엔진을 식별합니다.

- Unreal: `*.uproject`, `Config/`, `Content/`, `Source/`, `.uplugin`
- Unity: `ProjectSettings/ProjectVersion.txt`, `Assets/`, `Packages/manifest.json`

둘 다 존재하면 파일이나 엔진 상태를 변경하기 전에 어떤 workspace를 수정하는지 먼저 명시합니다.

## 필요한 로컬 스킬

다음 작업을 하기 전에 로컬 game skills를 사용합니다.

- 게임 설계, 기능 설계, 시스템 설계, 문서 갱신: `game-docs-maintaining`
- Unreal/Unity MCP 설정, 에디터 작업, 엔진 소유 에셋, 에디터 상태 확인: `game-engine-mcp-operating`
- Unreal MCP 전용 작업: `game-engine-mcp-operating` 다음에 `unreal-mcp-workflow`
- Unity MCP 전용 작업: `game-engine-mcp-operating` 다음에 `unity-mcp-workflow`, 그리고 MCPForUnity가 설치한 `.codex/skills/unity-mcp-skill/SKILL.md`의 `unity-mcp-orchestrator`
- 씬, 레벨, prefab, actor, GameObject, UI 계층 작업: `game-scene-ui-iteration`
- 테스트, 플레이테스트, 버그 재현, 콘솔 오류, 검증 증거: `game-playtesting-and-validation`
- HUD, menu, UI Toolkit, uGUI, UMG, CommonUI, runtime UI binding, focus/navigation 변경: `game-ui-implementation`, 함께 `game-scene-ui-iteration`, `game-playtesting-and-validation`, 필요 시 `game-localization-accessibility`
- Import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, asset naming/folders 변경: `game-asset-pipeline`, 함께 `game-engine-mcp-operating`, engine workflow, 필요 시 `game-content-branching-and-merging`
- FPS, frame time, memory, hitches, draw calls, shader cost, load time, build size, profiling 변경: `game-performance-budgeting`, 함께 `game-playtesting-and-validation`, `game-docs-maintaining`
- Save schema, persistence format, player progression data, migration, backward compatibility 변경: `game-save-data-migrations`, 함께 `game-playtesting-and-validation`, `game-docs-maintaining`
- Player controls, input mapping, Unity Input System, Unreal Enhanced Input, camera state, aiming, lock-on 변경: `game-input-and-camera-design`, 함께 `game-ui-implementation`, `game-playtesting-and-validation`, 필요 시 `game-localization-accessibility`
- AI behavior, Behavior Tree, state machine, NavMesh, perception, blackboard, spawn logic 변경: `game-ai-behavior-debugging`, 함께 `game-scene-ui-iteration`, `game-playtesting-and-validation`
- Multiplayer, authority, ownership, replication, prediction, rollback, matchmaking state 변경: `game-networking-authority`, 함께 `game-playtesting-and-validation`, `game-docs-maintaining`
- Binary engine assets, locks, prefab/Blueprint merge conflicts, Unreal OFPA, Unity YAML conflicts 변경: `game-content-branching-and-merging`, 함께 `game-asset-pipeline`, `game-engine-mcp-operating`
- Localization keys, translated text, font fallback, subtitles, readability, colorblind support, safe areas 변경: `game-localization-accessibility`, 함께 `game-ui-implementation`, `game-input-and-camera-design`

## Superpowers 단계별 game skill routing

이 extension의 자동 선택은 runtime hook이 아니라 instruction-based activation입니다. 사용자가 skill 이름을 직접 부르지 않아도, 요청이 game domain artifact나 behavior를 바꾸면 `SKILL.md` description과 이 routing으로 관련 local skill을 함께 선택합니다.

| Superpowers 단계 | 자동으로 확인할 game skill | 적용 방식 |
|---|---|---|
| Task intake / skill check | 모든 game skills | 요청에 game domain artifact나 behavior 변경이 있으면 관련 local skill을 선택합니다. |
| `brainstorming` | `game-docs-maintaining`, 관련 domain skill | 기획, UI, input, save, AI, networking, performance, asset, accessibility 영향이 있으면 관련 docs와 domain constraints를 설계 질문에 반영합니다. |
| `writing-plans` | `game-docs-maintaining`, `game-playtesting-and-validation`, 관련 domain skill | 구현 계획에 docs update, editor/MCP preflight, validation evidence, rollback task를 포함합니다. |
| `test-driven-development` | `game-playtesting-and-validation`, domain-specific validation skill | Compile만으로 완료하지 않고 domain별 evidence를 계획합니다. |
| `subagent-driven-development` / `executing-plans` | 작업 파일과 engine에 맞는 domain skill | Subtask가 UI, asset, save, input, AI, networking, localization, performance에 닿으면 해당 skill 지침을 적용합니다. |
| Engine/MCP 작업 전 | `game-engine-mcp-operating`, engine workflow, 관련 domain skill | Editor 상태, project route, read-only query, snapshot, rollback를 먼저 확인합니다. |
| Code review | `game-docs-maintaining`, `game-playtesting-and-validation`, 관련 domain skill | docs drift, missing validation, unsafe asset edit, domain-specific regression risk를 review risk로 봅니다. |
| `verification-before-completion` | `game-playtesting-and-validation`, `game-docs-maintaining`, 관련 domain skill | 완료 주장 전에 compile/test/log/screenshot/docs/evidence 중 필요한 fresh evidence를 확인합니다. |
| `finishing-a-development-branch` | `game-docs-maintaining`, `game-content-branching-and-merging` | docs map, change log, decision log, generated files exclusion, binary asset policy를 최종 확인합니다. |

## 살아 있는 게임 문서

`docs/game/`를 최신 상태로 유지합니다. 게임 규칙, UX 흐름, 씬 구조, 시스템 아키텍처, 엔진 통합, 테스트, 검증 전략에 영향을 주는 변경은 같은 작업에서 관련 문서를 함께 갱신해야 합니다.

Mermaid는 게임플레이 루프, UI 흐름, 씬 전환, 상태 머신, 아키텍처 다이어그램을 문장보다 더 명확하게 보여줄 때만 사용합니다.

## 살아 있는 게임 문서 자동 확인

- `brainstorming`: game design, UI, scene, asset, save, performance, input, AI, networking, accessibility에 영향이 있으면 `docs/game/00-index.md`와 관련 docs를 먼저 확인합니다.
- `writing-plans`: 구현 계획에 필요한 docs update, `change-log.md`, `decision-log.md` 작업을 명시합니다.
- `subagent-driven-development` / `executing-plans`: subtask가 game behavior나 engine content를 바꾸면 같은 task 안에서 관련 living docs 갱신 여부를 확인합니다.
- Code review: docs drift, stale `00-index.md`, missing validation evidence, missing change-log entry를 review risk로 다룹니다.
- `verification-before-completion`: 완료 주장 전에 관련 docs update 또는 no-op 이유를 fresh evidence로 확인합니다.
- `finishing-a-development-branch`: `docs/game/00-index.md`, `change-log.md`, `decision-log.md`, 신규 docs template 포함 여부를 최종 확인합니다.

## 엔진 에셋 안전

바이너리 엔진 에셋은 직접 편집하지 않습니다. Unreal의 `.uasset`과 `.umap`은 editor, MCP, commandlets, 또는 문서화된 engine tooling을 사용합니다. Unity의 `.unity`, `.prefab`, `.asset`, `.meta`는 가능하면 Unity Editor APIs 또는 MCP를 사용합니다. Direct YAML edits는 text serialization이 활성화되어 있고, 변경 범위가 작으며, editor가 결과를 검증할 수 있을 때만 허용합니다.

파괴적인 씬, 콘텐츠, UI 변경 전에는 현재 상태를 스냅샷으로 남기고 롤백 방법을 설명하며, 실험에는 복제한 씬, 레벨, 프리팹을 우선 사용합니다.

## MCP 안전

Unreal MCP와 Unity MCP는 로컬 에디터 자동화 표면입니다. 도구 호출 전에 에디터가 실행 중인지, 올바른 프로젝트 또는 인스턴스가 활성화되어 있는지, 그리고 MCP server가 읽기 전용 쿼리에 응답하는지 확인합니다.

인증되지 않은 로컬 engine MCP 포트를 네트워크에 노출하지 않습니다. local MCP endpoint는 localhost 전용으로 취급합니다.

여러 Unity Editor 인스턴스가 있으면 수정 전에 활성 인스턴스를 지정합니다. Unreal MCP에서는 중복 도구 호출을 피하고 editor tool calls를 직렬 작업으로 취급합니다.

Unity 프로젝트에서 MCPForUnity를 설치하고 설정하면 `.codex/skills/unity-mcp-skill/SKILL.md`가 생성되며, 해당 skill의 frontmatter name은 `unity-mcp-orchestrator`입니다. Unity MCP tool/resource 세부 절차는 이 MCPForUnity local skill을 따르고, game extension skills는 게임 문서, scene/UI 안전, 검증 증거를 조율합니다.

## 완료의 의미는 검증됨

파일 편집만으로 완료를 선언하지 않습니다. 완료에는 적절한 컴파일, 에디터 새로고침, 씬 검증, 테스트, 콘솔 또는 로그 확인, 문서 갱신 조합이 필요합니다.
