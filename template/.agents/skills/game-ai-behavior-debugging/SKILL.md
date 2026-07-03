---
name: game-ai-behavior-debugging
description: Use when changing AI behavior, Behavior Trees, state machines, NavMesh, pathfinding, perception, blackboards, utility AI, spawn logic, or enemy debugging.
---

# Game AI Behavior Debugging

## Overview

AI behavior 변경은 expected decision, state, perception, navigation, target selection을 분리해서 검증해야 한다. Engine-specific surface는 확인하되 API manual을 복제하지 않는다.

## Workflow

1. Expected AI behavior를 state, perception, navigation, target selection, combat decision으로 분해한다.
2. Unity NavMesh/Animator/state machine 또는 Unreal Behavior Tree/Blackboard/EQS 같은 surface를 식별한다.
3. Repro scene/path와 expected decision을 문서화한다.
4. Spawn/despawn, stuck behavior, target switching 같은 edge behavior를 함께 확인한다.
5. 변경 후 `docs/game/04-gameplay-systems.md` 갱신을 유도한다.

## Verification

- Repro scene/path와 expected AI decision을 기록한다.
- Navigation, line of sight, target selection, stuck behavior, spawn/despawn을 확인한다.
- AI 변경 후 console/log와 playtest evidence를 남긴다.
- Non-deterministic AI라면 seed, scenario, repeated run 여부를 가능한 범위에서 기록한다.
