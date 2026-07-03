---
name: game-networking-authority
description: Use when changing multiplayer networking, authority, ownership, replication, prediction, rollback, matchmaking state, or deterministic gameplay tests.
---

# Game Networking Authority

## Overview

Multiplayer 변경은 one-client success로 완료되지 않는다. Authority, ownership, replication, prediction, reconciliation, disconnect behavior를 명확히 나눈다.

## Workflow

1. Authority model, ownership, replication boundary, client prediction, reconciliation을 명확히 한다.
2. Single-player code path와 multiplayer code path의 divergence를 추적한다.
3. Network state가 gameplay, UI, save/progression에 주는 영향을 확인한다.
4. 변경 후 `docs/game/02-gameplay-design.md`와 필요 시 `docs/game/04-engine-architecture.md` 갱신을 유도한다.

## Verification

- Host/client, dedicated server, listen server 중 검증 환경을 명시한다.
- One-client success만으로 완료하지 않고 최소 two-client smoke path를 고려한다.
- Race condition, desync, ownership transfer, late join, disconnect behavior를 기록한다.
- Deterministic test가 불가능하면 manual smoke의 한계와 remaining risk를 남긴다.
