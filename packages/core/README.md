# leanscene-core (free, MIT)

Pure logic. **No `unreal` import, ever** (ADR-002) — enforced in CI by
`tools/check_no_unreal_import.py`.

Today this package holds:
- **`UnrealGateway`** — the single coarse interface to the editor, plus the plain
  record types it returns (`ActorRecord`, `AssetRecord`, `LevelSummary`).
- **Token meter** — offline, deterministic token counting (`TokenMeter`,
  `TiktokenCounter`). The default backend is a *proxy* tokenizer using a vendored
  tiktoken encoding (no network). Exact Claude counts are a networked stub
  (`AnthropicTokenCounter`) — see ADR-003.

Schema shapers, the shadow estimator, and the diff engine land here in later
tasks. Everything is testable headless.
