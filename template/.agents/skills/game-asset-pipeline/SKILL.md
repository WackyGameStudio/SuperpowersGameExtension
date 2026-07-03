---
name: game-asset-pipeline
description: Use when changing asset import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, naming, folder taxonomy, source/generated policy, or reference integrity.
---

# Game Asset Pipeline

## Overview

Asset import settings, naming, folders, references, source/generated policy는 runtime behavior와 source control 상태를 동시에 바꿀 수 있다. Engine-owned asset은 direct text edit보다 editor, MCP, commandlet, engine API를 우선한다.

## Workflow

1. Source asset과 generated/imported asset을 구분한다.
2. Naming, folder taxonomy, GUID/reference safety, import settings, material/texture/audio policy를 확인한다.
3. Unity prefab/ScriptableObject와 Unreal Blueprint/Data Asset의 editor-owned 변경 경계를 명확히 한다.
4. Binary asset 변경은 direct edit가 아니라 editor/MCP/tooling path를 우선한다.
5. Branch, merge, lock 문제로 번지면 `game-content-branching-and-merging`을 함께 사용한다.
6. 변경 후 `docs/game/03-content-and-ux.md` 갱신 여부를 판단한다.

## Verification

- Missing references, broken prefab/Blueprint links, unintended `.meta` churn, redirector 문제를 확인한다.
- Large binary asset 변경은 rollback 경로와 source control 정책을 확인한다.
- Asset 변경이 runtime behavior에 영향을 주면 `game-playtesting-and-validation`으로 연결한다.
- Generated directories가 commit 대상에 섞이지 않았는지 확인한다.
