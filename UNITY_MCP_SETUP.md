# Unity MCP 설정 가이드

이 문서는 `superpowers-game-extension`을 Unity 프로젝트에서 editor 제어와 함께 쓰기 위한 MCP 전제조건을 정리합니다.

이 extension은 Unity MCP를 직접 설치하지 않습니다. Unity Editor를 AI agent가 제어하려면 대상 Unity 프로젝트에 [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)를 먼저 설정해야 합니다.

English version: [UNITY_MCP_SETUP.en.md](UNITY_MCP_SETUP.en.md)

## 왜 먼저 필요한가

`superpowers-game-extension`은 게임 개발 workflow, 문서화, 안전 규칙을 설치합니다. 하지만 Unity Editor의 scene, GameObject, asset, console, Play Mode 상태를 실제로 읽거나 제어하려면 Unity MCP가 필요합니다.

Unity MCP가 설정되지 않은 상태에서도 문서와 코드 작업은 가능하지만, editor 상태 확인과 자동화는 제한됩니다.

## 기준 문서

- [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)

CoplayDev README 기준 Quickstart는 Unity 2021.3 LTS부터 Unity 6.x, Python 3.10+와 `uv`를 요구하며, Unity Package Manager에서 git URL로 package를 추가한 뒤 Unity 메뉴에서 client 설정을 생성하는 흐름입니다.

CoplayDev README는 `#main` 설치도 안내하지만, 이 가이드에서는 재현성을 위해 release tag pin을 권장합니다. 설치 시점에 [CoplayDev/unity-mcp Releases](https://github.com/CoplayDev/unity-mcp/releases)에서 최신 stable release tag를 확인하세요.

## 설정 절차

1. 대상 Unity 프로젝트를 Unity Editor로 엽니다.

2. Unity Package Manager에서 package를 추가합니다.

   Unity 메뉴에서 `Window > Package Manager`를 열고 `Add package from git URL...`을 선택한 뒤 release tag를 pin한 URL을 입력합니다.

   ```text
   https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#<latest-release-tag>
   ```

   예를 들어, 2026-07-03 기준 최신 release는 `v10.0.0`이므로 다음 형태입니다. 실제 설치 전에는 GitHub Releases에서 최신 tag를 다시 확인하세요.

   ```text
   https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.0.0
   ```

   `#main`은 항상 최신 development 상태를 따라가는 moving target입니다. 팀 프로젝트나 재현 가능한 환경이 필요하면 `#main` 대신 release tag를 사용합니다.

3. MCP for Unity 창을 엽니다.

   ```text
   Window > MCP for Unity > Toggle MCP Window
   ```

   처음 열면 보통 `Connect` 탭이 표시됩니다.

4. `Connect` 탭에서 server 상태와 client 설정을 확인합니다.

   - Server가 꺼져 있으면 켭니다.
   - 필요한 AI/MCP client를 개별로 configure합니다.
   - 전체 client를 한 번에 설정하려면 `Configure All Detected Clients`를 사용합니다.
   - MCP for Unity가 제공하는 local skill pack을 쓰려면 `Install Skill`을 실행합니다.

   `Install Skill`이 성공하면 Unity 프로젝트에 MCPForUnity local skill이 설치됩니다. 이 extension의 Unity workflow는 그 skill과 함께 `docs/game`, scene/UI 안전, 검증 증거를 조율합니다.

5. `Tools` 탭에서 tool 노출을 확인합니다.

   `Tools` 탭은 AI agent가 호출할 수 있는 Unity Editor tool 목록을 관리하는 곳입니다. scene, GameObject, asset, console, test 같은 editor 작업을 agent가 수행하려면 필요한 tool이 활성화되어 있어야 합니다.

   이 extension과 함께 처음 설정할 때는 `Enable All`을 권장합니다. 이후 팀 정책에 따라 필요한 tool만 남기고 줄일 수 있습니다.

6. `Resources` 탭에서 resource 노출을 확인합니다.

   `Resources` 탭은 AI agent가 읽기 전용으로 가져올 수 있는 Unity project/editor 정보 목록을 관리하는 곳입니다. project info, editor state, scene/camera 정보 같은 context 확인에 사용됩니다.

   처음 설정할 때는 `Enable All`을 권장합니다. Read-only context가 충분해야 agent가 변경 전에 현재 상태를 확인할 수 있습니다.

7. `Deps` 탭에서 dependency를 설치합니다.

   `Deps` 탭은 MCP for Unity가 동작하는 데 필요한 dependency를 확인하고 설치하는 곳입니다. Python/uv 등 client/server 실행에 필요한 구성 요소가 여기서 관리될 수 있습니다.

   처음 설정할 때는 `Install All`을 실행합니다. 설치 후 에러가 남아 있으면 해당 항목의 안내에 따라 해결합니다.

8. `Advanced` 탭은 기본적으로 건드리지 않습니다.

   `Advanced` 탭은 세부 설정과 진단용 옵션을 다루는 곳입니다. port, transport, low-level 동작을 바꿀 필요가 있는 경우가 아니라면 기본값을 유지합니다.

9. AI coding agent를 대상 Unity 프로젝트 루트에서 실행합니다.

   agent가 MCP client 설정을 읽을 수 있도록 Unity 프로젝트 루트에서 실행하는 것을 권장합니다.

10. 연결을 확인합니다.

   agent에게 다음처럼 read-only 확인을 요청합니다.

   ```text
   Unity MCP 연결을 확인하고 현재 active scene, Play Mode 상태, console error를 읽기 전용으로 확인해줘.
   ```

## 설치 후 기대 상태

정상 설정되면 AI agent는 Unity Editor에 대해 다음 작업을 수행할 수 있습니다.

- active scene과 hierarchy 확인
- GameObject, camera, UI object 조회
- console error/warning 확인
- Play Mode/Edit Mode test 실행
- scene 또는 asset 변경 전 read-only 상태 확인

## MCP for Unity 탭 요약

| 탭 | 역할 | 권장 초기 설정 |
|---|---|---|
| `Connect` | MCP server on/off, client configure, skill install을 관리합니다. | Server를 켜고 필요한 client를 configure합니다. 필요하면 `Configure All Detected Clients`와 `Install Skill`을 실행합니다. |
| `Tools` | Agent가 호출할 수 있는 editor tool 목록을 관리합니다. | `Enable All` |
| `Resources` | Agent가 읽기 전용으로 가져올 수 있는 project/editor context를 관리합니다. | `Enable All` |
| `Deps` | MCP for Unity 실행에 필요한 dependency 설치/상태를 관리합니다. | `Install All` |
| `Advanced` | port, transport, 진단 등 고급 설정을 다룹니다. | 기본값 유지 |

## 안전 원칙

- 처음 연결 확인은 read-only 요청으로 시작합니다.
- scene, prefab, asset 변경 전에는 변경 범위와 rollback 방법을 먼저 확인합니다.
- 여러 Unity Editor instance가 열려 있으면 대상 project/instance를 명시합니다.
- MCP endpoint는 local 개발용으로 취급하고 외부 네트워크에 노출하지 않습니다.

## 이 extension 설치와의 관계

Unity MCP 설정이 끝난 뒤 [INSTALL_FOR_AI.md](INSTALL_FOR_AI.md)를 AI agent에게 읽게 해서 `superpowers-game-extension`을 대상 Unity 프로젝트에 설치하세요.

```text
WackyGameStudio/SuperpowersGameExtension의 INSTALL_FOR_AI.md를 읽고 이 Unity 프로젝트에 설치해줘.
```
