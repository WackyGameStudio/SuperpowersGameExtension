# superpowers-game-extension

`superpowers-game-extension`은 `Superpowers`에 게임 개발 맥락을 더하는 repo-local extension입니다.

이 저장소는 전역 `obra/superpowers` workflow를 바꾸지 않습니다. 대신 Unity/Unreal 게임 프로젝트 안에 `AGENTS.md`, `.agents/skills`, `docs/game` 템플릿을 설치해서 AI agent가 일반적인 `Superpowers` 흐름 안에서 게임 개발용 문서화, 엔진 확인, 검증 절차를 함께 따르도록 합니다.

English version: [README.en.md](README.en.md)

## 왜 필요한가

`Superpowers`는 brainstorming, design/spec, plan, implementation, verification으로 이어지는 범용 개발 workflow로 유용합니다. 하지만 게임 개발에는 범용 코드 작업과 다른 별도 맥락이 필요하고, 코드 변경만으로 끝나지 않습니다.

게임 작업에는 Unity/Unreal editor 상태, scene/level 구조, asset import와 참조, playtest 결과, 성능 예산, input/camera 감각, save data, localization/accessibility 같은 맥락이 함께 따라옵니다. 일반 workflow만 쓰면 AI agent가 engine/editor 상태를 확인하지 못하거나, `docs/game` 같은 프로젝트 문서와 실제 구현 상태가 벌어지거나, MCP/Editor 조작을 안전하게 다루지 못할 수 있습니다.

이 extension은 그 간극을 줄이기 위해 만들었습니다.

## 어떻게 해결하나

설치하면 대상 게임 프로젝트에 repo-local 규칙과 game skills, living docs 템플릿이 들어갑니다.

```text
GameProject/
  AGENTS.md
  .agents/skills/
  docs/game/
```

사용자는 평소처럼 `Superpowers` 흐름으로 요청하면 됩니다. 예를 들어 브레인스토밍부터 구현과 검증까지 이어지는 작업을 자연어로 요청하면, 설치된 `AGENTS.md`와 `SKILL.md` descriptions가 `instruction-based activation` 방식으로 관련 game skill을 선택하게 안내합니다.

이때 extension은 두 가지를 중심으로 돕습니다.

- `docs/game` living docs를 갱신해서 사람과 AI가 같은 게임 설계, 구현 상태, 검증 근거를 읽게 합니다.
- Unity/Unreal MCP workflow와 안전 규칙을 연결해서 editor 상태 확인, read-only probe, mutating action 승인, 검증 증거를 놓치지 않게 합니다.

이 저장소는 Unity/Unreal MCP 자체를 설치하지 않습니다. MCPForUnity, Unreal MCP 같은 engine integration은 대상 게임 프로젝트 환경에서 별도로 설정합니다.

## Quick Start

1. Editor 제어가 필요하면 engine MCP를 먼저 설정합니다. 이 단계가 완료돼야 AI agent가 Unity/Unreal Editor 상태를 읽고 scene, actor, asset, console, test 같은 editor 작업을 제어할 수 있습니다.

   - Unity 프로젝트: [Unity MCP 설정 가이드](UNITY_MCP_SETUP.md)
   - Unreal 프로젝트: [Unreal MCP 설정 가이드](UNREAL_MCP_SETUP.md)

2. 대상 Unity/Unreal 프로젝트를 열고 AI coding agent에게 [INSTALL_FOR_AI.md](INSTALL_FOR_AI.md)를 읽게 해서 extension 설치를 맡깁니다.

```text
WackyGameStudio/SuperpowersGameExtension의 INSTALL_FOR_AI.md를 읽고 이 게임 프로젝트에 설치해줘.
```

AI agent는 `template/` 아래 파일을 대상 프로젝트에 안전하게 복사합니다. 기존 `AGENTS.md`가 있으면 내용을 지우지 않고 아래에 game extension 지침을 추가합니다.

3. 설치 후에는 일반 `Superpowers` 사용 방식처럼 요청합니다.

```text
이 Unity 프로젝트의 combat loop를 브레인스토밍부터 구현 계획까지 같이 정리해줘.
```

```text
Unreal 프로젝트의 HUD 흐름을 점검하고, 필요한 문서와 검증 절차까지 같이 업데이트해줘.
```

MCP 설정 없이도 문서/코드 작업은 가능하지만, editor 상태 확인과 자동화는 제한됩니다.

## 설치하면 생기는 것

설치 payload의 source of truth는 이 저장소의 `template/`입니다.

```text
template/
  AGENTS.md
  .agents/skills/
  docs/game/
```

대상 게임 프로젝트에는 다음 파일과 디렉터리가 생성됩니다.

| 경로 | 역할 |
|---|---|
| `AGENTS.md` | 게임 프로젝트임을 식별하고, Superpowers 단계별로 필요한 local game skill을 선택하도록 안내합니다. |
| `.agents/skills/` | Unity/Unreal, scene/UI, asset, performance, save data, input/camera, AI, networking, localization/accessibility 작업용 local skills입니다. |
| `docs/game/` | 게임 설계, 시스템, scene, UI flow, asset policy, architecture, save model, QA, performance, release 정보를 담는 living docs 템플릿입니다. |

AI 설치 절차는 비파괴가 기본입니다. 대상 프로젝트에 같은 경로의 `.agents/skills` 또는 `docs/game` 파일이 이미 있으면 덮어쓰지 않고 conflict로 보고해야 합니다. 이 extension repo 루트에는 `.agents/`와 `AGENTS.md`를 만들지 않습니다. 개발 중인 local skill이 현재 Codex 세션에 자동 로드되는 것을 피하기 위한 root safety 제약입니다.
`INSTALL_FOR_AI.md` 방식에서는 `AGENTS.md`만 append-only로 특별 취급합니다. `.agents/skills`와 `docs/game`는 기존 파일을 덮어쓰지 않고 누락된 파일만 복사하거나 충돌을 보고합니다.

## 사용 방식

사용자가 game skill 이름을 직접 외울 필요는 없습니다. 설치된 `AGENTS.md`는 일반 `Superpowers` 단계에 game domain routing을 더합니다.

| Superpowers 단계 | extension이 추가로 확인하는 것 |
|---|---|
| brainstorming | 게임 설계, UI, scene, asset, save, performance, input, AI, networking, accessibility 영향과 관련 docs를 확인합니다. |
| design/spec | 게임 규칙, UX flow, engine constraints, 검증 방법을 living docs와 연결합니다. |
| writing-plans | docs update, editor/MCP preflight, validation evidence, rollback task를 계획에 포함하게 합니다. |
| implementation | 작업 파일과 engine domain에 맞는 local skill 지침을 적용합니다. |
| verification | compile/test만 보지 않고 playtest, editor log, screenshot, docs update 같은 fresh evidence를 요구합니다. |

즉, 평소처럼 `Superpowers`를 사용하면 됩니다. 이 extension은 게임 개발에서 빠지기 쉬운 문서화와 engine/editor 안전 확인을 local instruction으로 보강합니다.

## Unity/Unreal MCP와 안전 규칙

Unity/Unreal MCP는 local editor automation 표면입니다. 이 extension은 MCP를 직접 설치하지 않고, MCP를 사용할 때 어떤 순서와 안전 기준을 따라야 하는지 game workflow에 연결합니다.

기본 원칙은 다음과 같습니다.

- editor가 실행 중인지, 올바른 project/instance가 활성화되어 있는지 먼저 확인합니다.
- mutating tool call 전에 read-only query와 현재 상태 snapshot을 우선합니다.
- binary engine assets는 직접 텍스트 편집하지 않고 editor, MCP, commandlet, 문서화된 engine tooling을 우선합니다.
- 여러 Unity Editor 인스턴스나 Unreal MCP toolset이 있을 때는 대상 project와 toolset을 명시합니다.
- local MCP endpoint는 localhost 전용으로 취급하고 네트워크에 노출하지 않습니다.

Unity 프로젝트에서 MCPForUnity를 설치하면 `.codex/skills/unity-mcp-skill/SKILL.md`가 생성되며, 해당 skill의 frontmatter name은 `unity-mcp-orchestrator`입니다. 이 extension의 Unity workflow는 그 local skill pack과 함께 게임 문서, scene/UI 안전, 검증 증거를 조율합니다.

## Living Docs

`docs/game`은 사람과 AI가 함께 보는 살아 있는 게임 문서입니다. 게임 규칙, UX 흐름, scene 구조, system architecture, engine integration, QA, performance budget, release constraints가 바뀌면 같은 작업에서 관련 문서를 함께 갱신하는 것을 목표로 합니다.

기본 문서 맵은 다음과 같습니다.

- `00-index.md`: 프로젝트 식별, 문서 맵, 현재 검증 상태
- `01-vision-and-pillars.md`: 목표 경험, 설계 원칙, 비목표
- `02-core-loop.md`: core loop, session loop, reward loop
- `03-player-and-controls.md`: player verbs, input mapping, camera state, accessibility controls
- `04-gameplay-systems.md`: combat, AI, progression, multiplayer authority, validation path
- `05-scenes-and-levels.md`: scenes, levels, maps, transitions
- `06-ui-ux-flow.md`: HUD, menus, modal stack, routing, focus behavior
- `07-content-and-assets.md`: asset taxonomy, naming, source/generated policy, reference integrity
- `08-technical-architecture.md`: runtime modules, editor tools, engine integration
- `09-data-and-save-model.md`: save schema, migrations, compatibility, save/load validation
- `10-playtest-and-qa.md`: smoke tests, bug reproduction, validation evidence
- `11-performance-budgets.md`: target platform, frame/memory/loading budgets, measurement results
- `12-build-release-platforms.md`: build scenes/maps, packaging constraints, pre-release checks
- `decision-log.md`: 중요한 결정과 trade-off
- `change-log.md`: 게임 의미가 있는 변경 사항

## 포함된 game skills

설치되는 `.agents/skills`는 다음 game domain을 다룹니다.

| Skill | 적용 대상 |
|---|---|
| `game-docs-maintaining` | design, gameplay rules, scenes, UI flow, content, architecture, save data, testing, performance, build targets, project documentation |
| `game-engine-mcp-operating` | Unreal/Unity MCP 연결, editor tools, engine-owned assets, scene inspection, editor state validation |
| `unity-mcp-workflow` | Unity MCP, Unity Editor automation, scenes, GameObjects, prefabs, ScriptableObjects, uGUI, UI Toolkit, Play Mode, Edit Mode tests |
| `unreal-mcp-workflow` | Unreal MCP, Unreal Editor automation, levels, actors, Blueprints, UMG, CommonUI, materials, PIE, Automation tests |
| `game-scene-ui-iteration` | levels, scenes, actors, GameObjects, prefabs, widgets, canvases, UIDocuments, menus, HUDs, visual hierarchy |
| `game-playtesting-and-validation` | gameplay verification, bug reproduction, Unity tests, Unreal Automation tests, smoke tests, editor log checks |
| `game-ui-implementation` | HUDs, menus, UI Toolkit, uGUI, UMG, CommonUI, navigation, focus, runtime UI binding |
| `game-asset-pipeline` | import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, asset naming/folders |
| `game-performance-budgeting` | FPS, frame time, hitches, memory, draw calls, shader cost, loading time, build size, profiling |
| `game-save-data-migrations` | save schema, persistence format, progression data, migrations, backward compatibility, save/load tests |
| `game-input-and-camera-design` | player controls, input mapping, Unity Input System, Unreal Enhanced Input, camera states, aiming, lock-on |
| `game-ai-behavior-debugging` | Behavior Trees, state machines, NavMesh, pathfinding, perception, blackboards, spawn logic |
| `game-networking-authority` | multiplayer authority, ownership, replication, prediction, rollback, matchmaking, deterministic tests |
| `game-content-branching-and-merging` | binary engine assets, asset locks, prefab/Blueprint conflicts, Unreal OFPA, Unity YAML conflicts |
| `game-localization-accessibility` | localization keys, translated text, font fallback, subtitles, readability, colorblind support, input accessibility, safe areas |

## 개발자 참고

이 extension repo 자체의 루트에는 `.agents/`와 `AGENTS.md`를 만들지 않습니다. 설치 payload는 항상 `template/` 아래에서 관리합니다. 이 제약은 extension을 개발하는 Codex 세션이 아직 검증 중인 local skill을 자동 로드하지 않게 하기 위한 것입니다.

Codex plugin packaging은 아직 일반 설치 흐름이 아닙니다. 현재 기본 사용 경로는 `INSTALL_FOR_AI.md`를 AI coding agent에게 읽게 해서 대상 게임 프로젝트에 repo-local `AGENTS.md`, `.agents/skills`, `docs/game`를 설치하는 방식입니다.
