---
name: game-save-data-migrations
description: Use when changing save data schema, persistence format, player progression data, migration logic, backward compatibility, or save/load tests in a game.
---

# Game Save Data Migrations

## Overview

Save schema와 migration 변경은 player data loss risk가 크다. Runtime data model tuning와 persistence compatibility를 분리해서 판단한다.

## Workflow

1. Save schema 변경과 runtime data model 변경을 구분한다.
2. Version tagging, backward compatibility, migration path, corrupt save handling을 확인한다.
3. Migration은 player data loss risk가 있으므로 `docs/game/decision-log.md` 기록 후보로 본다.
4. Save model 변경 후 `docs/game/09-data-and-save-model.md` 갱신을 유도한다.

## Verification

- Old save fixture, new save fixture, migration result를 확인한다.
- Save/load roundtrip과 missing/corrupt data behavior를 검증한다.
- Migration failure 시 fallback, error messaging, data preservation policy를 명시한다.
- Manual validation만 가능하면 fixture 부재와 남은 risk를 최종 응답에 남긴다.
