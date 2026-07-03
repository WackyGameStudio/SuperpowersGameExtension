# Engine Architecture

## Engine identity

- Engine: 아직 감지되지 않음
- Engine version: 아직 기록되지 않음
- Primary project file: 아직 기록되지 않음

## Runtime modules and plugins

| Module or plugin | Responsibility | Depends on | Notes |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Editor tools and integration points

| Tool or integration | Purpose | Mutating actions allowed | Verification path |
|---|---|---|---|
| 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 | 아직 기록되지 않음 |

## Data ownership boundaries

아직 기록되지 않음.

## Save schema and migration policy

- Current save schema: 아직 기록되지 않음
- Backward compatibility contract: 아직 기록되지 않음
- Migration validation path: 아직 기록되지 않음

## Networking authority summary

아직 기록되지 않음.

## Engine-owned asset source control policy

- Unity `.meta` files: version control에 포함
- Unity scene/prefab/asset edits: 가능하면 Unity Editor API 또는 MCP를 사용
- Unreal `.uasset` and `.umap` edits: Unreal Editor, MCP, commandlets, 또는 문서화된 engine tooling 사용
- Unreal OFPA/external actor files: Editor/source control integration에서 변경 목록을 검증하고 submit 전에 level/actor reference 상태를 확인
- Generated files: source/generated policy가 기록될 때까지 commit 전에 검토

## Split notes

Runtime modules, save data, online authority, backend/live ops, or editor tooling details move to `architecture/` or `online/` only when the split criteria in `00-index.md` are met.
