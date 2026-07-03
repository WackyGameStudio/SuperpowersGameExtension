# Unreal MCP 설정 가이드

이 문서는 `superpowers-game-extension`을 Unreal 프로젝트에서 editor 제어와 함께 쓰기 위한 MCP 전제조건을 정리합니다.

이 extension은 Unreal MCP를 직접 설치하거나 활성화하지 않습니다. Unreal Editor를 AI agent가 제어하려면 Epic의 [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) 문서를 기준으로 대상 Unreal 프로젝트에 Unreal MCP를 먼저 설정해야 합니다.

English version: [UNREAL_MCP_SETUP.en.md](UNREAL_MCP_SETUP.en.md)

## 왜 먼저 필요한가

`superpowers-game-extension`은 게임 개발 workflow, 문서화, 안전 규칙을 설치합니다. 하지만 Unreal Editor의 level, actor, Blueprint, Slate widget, automation test 같은 editor 기능을 실제로 읽거나 제어하려면 Unreal MCP가 필요합니다.

Unreal MCP가 설정되지 않은 상태에서도 문서와 코드 작업은 가능하지만, editor 상태 확인과 자동화는 제한됩니다.

## 기준 문서

- [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor)

Epic 문서 기준 Unreal MCP는 Unreal Editor process 안에 MCP server를 포함하고, local HTTP connection으로 MCP-compatible AI agent가 editor 기능을 호출할 수 있게 합니다. 문서에서는 experimental feature이므로 shipping에는 주의하라고 안내합니다.

## 설정 절차

1. 대상 Unreal 프로젝트를 Unreal Editor로 엽니다.

2. Unreal MCP와 AllToolsets plugin을 활성화합니다.

   ```text
   Edit > Plugins
   ```

   `Unreal MCP`를 검색하고 `Enabled`를 체크합니다. 이때 `Toolset Registry` plugin은 dependency로 자동 활성화됩니다.

   이어서 `AllToolsets`도 검색해서 `Enabled`를 체크합니다. Unreal MCP server 자체는 MCP 연결을 담당하고, 실제 editor toolsets/tools는 `AllToolsets`가 제공합니다. `AllToolsets`가 꺼져 있으면 agent가 연결돼도 사용할 수 있는 toolset이 없거나 매우 제한적일 수 있습니다.

   Prompt가 나오면 editor를 재시작합니다.

3. Auto Start Server를 설정합니다.

   ```text
   Edit > Editor Preferences > General > Model Context Protocol
   ```

   `Auto Start Server`를 켜면 editor launch 시 MCP server가 자동으로 시작됩니다. 기본 endpoint는 다음입니다.

   ```text
   http://127.0.0.1:8000/mcp
   ```

   필요하면 port와 URL path를 같은 panel에서 조정합니다.

4. 필요 시 수동으로 server를 시작합니다.

   Auto Start를 쓰지 않는 경우 editor console에서 실행합니다.

   ```text
   ModelContextProtocol.StartServer
   ```

   port를 지정하려면 다음처럼 실행합니다.

   ```text
   ModelContextProtocol.StartServer 8000
   ```

5. AI client config를 생성합니다.

   editor console에서 원하는 client 이름을 지정합니다.

   ```text
   ModelContextProtocol.GenerateClientConfig Codex
   ```

   여러 agent를 함께 설정하려면 다음을 사용합니다.

   ```text
   ModelContextProtocol.GenerateClientConfig All
   ```

   Epic 문서 기준 지원 client 이름은 `ClaudeCode`, `Cursor`, `VSCode`, `Gemini`, `Codex`, `All`입니다. JSON-format config는 기존 entry와 merge되지만, Codex CLI용 TOML config는 write-once로 동작할 수 있으므로 stale config가 있으면 직접 정리해야 합니다.

6. AI coding agent를 config가 생성된 project/workspace root에서 실행합니다.

7. 연결을 확인합니다.

   agent에게 다음처럼 read-only 확인을 요청합니다.

   ```text
   Unreal MCP 연결을 확인하고 현재 toolsets, editor 상태, 열린 level 정보를 읽기 전용으로 확인해줘.
   ```

   `list_toolsets` 결과가 비어 있거나 기대보다 지나치게 적으면 `AllToolsets` plugin이 활성화되어 있는지 다시 확인합니다.

## 설치 후 기대 상태

정상 설정되면 AI agent는 Unreal Editor에 대해 다음 작업을 수행할 수 있습니다.

- MCP server 연결 확인
- `AllToolsets`가 제공하는 toolset과 tool 목록 확인
- level, actor, Blueprint, UMG/CommonUI, material 관련 상태 조회
- automation test 또는 editor 상태 read-only 확인
- mutating tool call 전 project/level 상태 snapshot 확인

## 안전 원칙

- 처음 연결 확인은 read-only 요청으로 시작합니다.
- Unreal MCP tool call은 game thread에서 직렬 실행되는 것으로 보고 overlapping call을 피합니다.
- `.uasset`, `.umap` 같은 binary engine asset은 직접 텍스트 편집하지 않습니다.
- local MCP endpoint는 인증 없는 local development endpoint로 취급하고 외부 네트워크에 노출하지 않습니다.
- Unreal MCP와 관련 toolset API는 변경될 수 있으므로 agent에게 현재 toolset/schema를 먼저 확인하게 합니다.

## 이 extension 설치와의 관계

Unreal MCP 설정이 끝난 뒤 [INSTALL_FOR_AI.md](INSTALL_FOR_AI.md)를 AI agent에게 읽게 해서 `superpowers-game-extension`을 대상 Unreal 프로젝트에 설치하세요.

```text
WackyGameStudio/SuperpowersGameExtension의 INSTALL_FOR_AI.md를 읽고 이 Unreal 프로젝트에 설치해줘.
```
