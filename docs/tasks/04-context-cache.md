# Task 04 — Local context cache (Component D, PREMIUM anchor)

**Goal.** Compound savings across a session by detecting unchanged level sectors and short-circuiting re-queries. Strongest premium value; **most fragile component** in the product.

## Mechanism
- Use `core`'s diff engine: hash level sectors via the gateway's `get_world_state_hash(sector)`, store per-session.
- On a query whose sector is unchanged, serve cached shaped data instead of re-querying.
- Invalidate on detected change.

## The hard part — invalidation (RISK: Med–High)
Invalidation against **live, experimental** editor state is where this breaks. Requirements:
- Conservative by default: when unsure whether a sector changed, **invalidate** (correctness over savings).
- Extensive change-detection tests against fixtures simulating edits (move / add / delete / modify in a sector).
- Explicit handling of editor events that should bust the cache.

## Acceptance
- [ ] Diff/cache logic tested headless against fixtures simulating sector edits.
- [ ] Stale data is never served in the test matrix (conservative invalidation holds).
- [ ] Cache reports its own contribution to savings separately (and honestly).
- [ ] (Editor, manual) invalidation holds against real live edits.

## Timeline (ADR-006)
Premium anchor. If it risks the v1 date, defer to first fast-follow; ship the dynamic steering engine as the v1 premium instead. Do not let cache fragility delay a shippable v1.
