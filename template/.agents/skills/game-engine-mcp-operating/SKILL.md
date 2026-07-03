---
name: game-engine-mcp-operating
description: Use when connecting to Unreal or Unity MCP, using editor tools, changing engine-owned assets, inspecting scenes, or validating editor state through MCP.
---

# Game Engine MCP Operating

## Overview

Unreal/Unity MCP는 local editor automation surface다. 연결 확인, 대상 project 확인, read-only preflight, snapshot, rollback, validation을 거친 뒤 작은 단위로 사용한다.

## Workflow

1. Repository evidence로 engine을 식별한다.
2. Editor가 실행 중이고 대상 project가 맞는지 확인한다.
3. MCP server가 read-only query에 응답하는지 확인한다.
4. 여러 editor instance가 가능하면 대상 instance를 고정한다.
5. Unity 프로젝트의 read-only preflight resource 선택, instance 확인, MCPForUnity 세부 절차는 `.codex/skills/unity-mcp-skill/SKILL.md`의 `unity-mcp-orchestrator`에 위임한다.
6. Unreal 작업은 `unreal-mcp-workflow`에서 Tool Search mode와 read-only/mutating guardrail을 따른다.
7. `tools/list` meta-tool 3개만 보고 blocker로 판단하지 않는다.
8. Unreal-specific toolset inspection은 `unreal-mcp-workflow`에 위임한다.
9. `game-engine-mcp-operating`은 대상 project 확인, snapshot 시점, rollback 경로, validation 범위를 조율한다.
10. 변경 전 scene, selected objects, relevant assets, console/log 상태를 snapshot한다.
11. 필요한 tool group이나 toolset만 활성화하거나 describe한다.
12. Engine-owned asset 변경은 editor/MCP/commandlet/API를 우선 사용한다.
13. 변경 후 editor refresh, compile, log check, test, docs update 중 필요한 항목을 수행한다.
14. Engine-owned asset 변경이 asset import, UI binding, AI behavior, networking, localization 같은 domain policy를 바꾸면 해당 domain skill을 함께 사용한다.

## Verification

- MCP 연결 실패 시 engine asset 변경을 진행하지 않는다.
- Destructive operation 전 rollback 경로를 사용자에게 설명한다.
- Unreal 작업은 `unreal-mcp-workflow`를 함께 사용한다.
- Unity 작업은 `unity-mcp-workflow`를 함께 사용한다.
- MCP endpoint는 localhost-only 전제로 다루며 네트워크 노출을 안내하지 않는다.
- Tool call은 target editor와 project identity가 확인된 뒤에만 실행한다.
