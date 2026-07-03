---
name: game-performance-budgeting
description: Use when working on FPS, frame time, hitches, memory, draw calls, shader cost, loading time, build size, profiling, or performance budgets in a game.
---

# Game Performance Budgeting

## Overview

Performance 작업은 감각적 추측이 아니라 target platform, budget, reproducible measurement path, before/after comparison으로 다룬다.

## Workflow

1. Target platform, scene/path, build/editor condition을 명시한다.
2. Frame, CPU, GPU, memory, loading, build size budget 중 이번 변경에 영향을 받는 항목을 고른다.
3. Optimization 전 baseline capture를 남긴다.
4. 변경 후 같은 scene/path/build condition에서 after capture를 남긴다.
5. Gameplay behavior가 바뀌면 `game-playtesting-and-validation` evidence도 요구한다.
6. `docs/game/11-performance-budgets.md`와 필요 시 `docs/game/12-build-release-platforms.md`를 갱신한다.

## Verification

- Baseline capture와 after capture를 비교한다.
- 측정 도구, scene/path, target platform, build/editor 여부를 기록한다.
- Budget을 만족하지 못하면 남은 bottleneck과 다음 측정 계획을 남긴다.
- 측정할 수 없는 환경이면 그 한계와 remaining risk를 최종 응답에 남긴다.
