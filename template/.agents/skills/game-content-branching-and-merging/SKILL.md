---
name: game-content-branching-and-merging
description: Use when working with binary engine assets, asset locks, prefab or Blueprint merge conflicts, Unreal OFPA, Unity YAML conflicts, source control layout, or content branch strategy.
---

# Game Content Branching and Merging

## Overview

Binary engine assets와 text-serialized assets는 collaboration risk가 다르다. Locks, branch strategy, generated files, conflict resolution, rollback을 먼저 정리한다.

## Workflow

1. Binary engine asset과 text-serialized asset의 collaboration risk를 구분한다.
2. Locking, branch strategy, merge ownership, generated files exclusion을 확인한다.
3. Unity `.meta`와 Unreal redirector/OFPA 같은 engine-specific collaboration 문제를 다룬다.
4. Import setting policy가 핵심이면 `game-asset-pipeline`을 함께 사용한다.
5. 변경 후 `docs/game/07-content-and-assets.md`와 필요 시 `decision-log.md` 갱신을 유도한다.

## Verification

- Merge/conflict 해결 전후 asset reference integrity를 확인한다.
- Generated directories가 commit 대상에 섞이지 않았는지 확인한다.
- Manual merge가 필요하면 rollback과 review path를 명시한다.
- Conflict 해결 후 engine/editor가 asset을 정상 load하는지 확인하거나, 확인하지 못한 이유를 남긴다.
