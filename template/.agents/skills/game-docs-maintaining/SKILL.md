---
name: game-docs-maintaining
description: Use when changing game design, gameplay behavior, content, UI/UX, engine architecture, save/network data, validation, performance, build targets, release constraints, or docs/game files.
---

# Game Docs Maintaining

## Overview

`docs/game/` is the compact source of truth for the game. Keep it accurate, searchable, and small enough to maintain. Prefer updating an existing core document over creating a new document.

## Core documents

Default docs:

- `00-index.md`
- `01-product-brief.md`
- `02-gameplay-design.md`
- `03-content-and-ux.md`
- `04-engine-architecture.md`
- `05-validation-release.md`
- `decision-log.md`
- `change-log.md`

## Workflow

1. Read `docs/game/00-index.md` first.
2. Identify which core document owns the changed game fact.
3. Read only the relevant core document and any expanded doc linked from the index.
4. If code/editor state and docs disagree, report the stale area before changing docs.
5. Update the smallest relevant section.
6. Update `decision-log.md` only for durable trade-offs or decisions likely to be debated again.
7. Update `change-log.md` only for player-facing or spec-level changes.
8. Do not create a new docs file unless the split criteria below are met.
9. If no docs update is needed, record the no-op reason in the final response.

## Split criteria

Create a new `docs/game` file only when at least one is true:

- The section is larger than about 150-200 lines.
- It has a separate owner/reviewer or QA matrix.
- It covers high-risk compatibility: save migration, networking, platform release, live ops, privacy, performance budget.
- It causes repeated PR conflicts or repeated design debates.
- It needs its own validation evidence ledger.

When splitting:

1. Move details to a focused file under `systems/`, `content/`, `ux/`, `architecture/`, `online/`, `validation/`, `platform/`, or `decisions/`.
2. Leave a short summary and link in the core document.
3. Register the new file in `00-index.md`.
4. Preserve old information unless explicitly superseded.

## Verification

- `00-index.md` matches actual docs files.
- Updated docs identify current status, owner if known, and last verified evidence if relevant.
- Markdown uses real line breaks and renderable headings/tables.
- No duplicate source of truth was created.
- Final response says which docs changed or why docs were not changed.
