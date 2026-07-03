---
name: unreal-mcp-workflow
description: Use when working with Unreal MCP, Unreal Editor automation, Unreal levels, actors, Blueprints, UMG, CommonUI, materials, PIE, or Automation tests.
---

# Unreal MCP Workflow

## Overview

Unreal MCP 작업은 Unreal Editor 안의 MCP server와 Toolset Registry를 local-only automation surface로 다룬다. `.uasset`와 `.umap`은 text editor로 직접 수정하지 않고, editor/MCP/API가 제공하는 경로로만 다룬다.

## Workflow

1. `*.uproject`, `Config/`, `Content/`, `Source/`, `.uplugin` evidence로 Unreal project를 확인한다.
2. Unreal Editor가 대상 project를 열고 있는지 확인한다.
3. MCP endpoint가 read-only query에 응답하는지 확인한다.
4. Tool Search mode를 기본값으로 가정한다.
5. `tools/list`가 `list_toolsets`, `describe_toolset`, `call_tool` 세 meta-tool만 반환해도 정상으로 본다.
6. `list_toolsets`로 Toolset Registry를 확인한다.
7. `describe_toolset`으로 필요한 toolset schema와 mutating 여부를 확인한다.
8. `call_tool`은 한 번에 하나씩 순차 실행한다.
9. Level, Actor, Material, Blueprint, Widget 변경 전에는 mutating operation gate를 통과한다.
10. 변경 후 save/compile/PIE/log/test 중 필요한 검증을 수행한다.
11. Scene/UI 영향은 `docs/game/05-scenes-and-levels.md` 또는 `docs/game/06-ui-ux-flow.md`와 맞춘다.

## Tool Search Mode

Unreal MCP는 `tools/list`에서 editor 기능 tool을 직접 모두 노출하지 않을 수 있다. `tools/list`가 meta-tool 3개만 반환하면 blocker로 판단하지 않는다.

Required sequence:

```text
tools/list
call_tool(list_toolsets)
call_tool(describe_toolset, <required toolset>)
call_tool(<toolset tool>, <minimal read-only args>)
```

Toolset 변경 직후 expected toolset이 보이지 않으면 editor restart, `ModelContextProtocol.RefreshTools`, client reconnect 중 어떤 조치가 필요한지 기록한다. Endpoint ground truth가 필요하면 MCP Inspector를 사용해 Codex agent 해석과 분리해서 확인한다.

## Required Read-only Probes

Required read-only probes는 mutating 작업 전에 가능한 범위에서 먼저 확인한다.

| 목적 | Toolset | 예시 tool |
|---|---|---|
| PIE 상태 | `EditorToolset.EditorAppToolset` | `IsPIERunning` |
| 선택 actor | `EditorToolset.EditorAppToolset` | `GetSelectedActors` |
| Content Browser path | `EditorToolset.EditorAppToolset` | `GetContentBrowserPath` |
| Output Log category | `EditorToolset.LogsToolset` | `GetLogCategories` |
| Output Log entries | `EditorToolset.LogsToolset` | `GetLogEntries` |
| Current level | `editor_toolset.toolsets.scene.SceneTools` | `get_current_level` |
| Automation tests | `AutomationTestToolset.AutomationTestToolset` | `ListTests` |
| PCG native nodes | `PCGToolset.PCGToolset` | `ListNativeNodes` |

`SlateInspectorToolset.SlateInspectorToolset`은 optional evidence로 사용할 수 있다. `Windows` 같은 read-only call은 허용하지만 click/type/drag는 mutating UI automation으로 취급한다.

## Mutating Operation Gate

PCG graph 생성, UMG widget 생성, Slate click/type/drag, Blueprint/asset/map 변경은 mutating operation으로 취급한다.

mutating operation 전에는 사용자 승인, snapshot, rollback 경로, validation plan을 먼저 남긴다. 변경 대상이 binary asset이면 source control 상태와 cleanup 가능성을 확인하고, 같은 editor session에서 overlapping tool call을 실행하지 않는다.

금지 기본값:

- `.uasset`, `.umap`을 text editor로 직접 수정
- 확인되지 않은 level/map에 actor 추가
- `Content`, `Config`, `Source`, `Plugins` 대량 변경
- PCG/Blueprint/UMG 생성 후 compile/save/test 생략
- Slate click/type/drag를 read-only 검증처럼 취급

## Volatile Output Policy

Unreal Editor가 정상 실행 중 갱신하는 runtime log는 source/content/config mutation과 분리한다.

Volatile runtime log allowlist:

```text
Saved/Logs/*.log
Saved/Logs/*-backup-*.log
```

`Saved/Logs/*.log` 변경은 `volatile_changed_files`로 기록한다. `Saved` 전체를 허용하지 않는다.

계속 hard forbidden으로 다루는 예:

- `Saved/Autosaves/**`
- `Saved/Backup/**`
- `Saved/Config/**`
- `Saved/Cooked/**`
- `Saved/StagedBuilds/**`
- `Saved/Logs` 아래 `.uasset`, `.umap`, `.ini`, `.json`, dump file, binary asset

## Verification

- `.uasset`와 `.umap`을 text editor로 수정하지 않는다.
- Unreal MCP tool call은 overlapping하지 않고 serial로 수행한다.
- `tools/list` meta-tool 3개만 보고 editor toolset 부재로 단정하지 않는다.
- Required read-only probes 중 성공한 항목과 실패한 항목을 최종 응답에 남긴다.
- World Partition, Data Layers, actor naming, actor folders, collision, navigation, UMG/CommonUI focus를 작업 성격에 맞게 확인한다.
- PIE, Automation Test, Functional Test, Output Log 중 수행한 검증과 한계를 최종 응답에 남긴다.
- Volatile log 외 forbidden write가 있으면 작업을 중단하고 evidence를 보존한다.
