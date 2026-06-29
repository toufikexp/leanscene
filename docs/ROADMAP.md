# Roadmap

> Reminder: the master spec's validation gate (§14) precedes building. If demand evidence (firehose pain + agentic-Unreal usage) is not confirmed, this build is premature. This roadmap assumes the gate passed.

## Build order (dependencies, not calendar)
1. **Foundation** (`docs/tasks/00-foundation.md`) — repo split, `UnrealGateway` interface, `FakeGateway` + first fixtures, token meter, CI with headless-only default + editor mark + the no-`unreal`-import check. Nothing else builds safely until this exists.
2. **MCP tools** (`01`) — the pinned v1 tool set, each with fixed schema + tuned description + per-call measurement envelope. Headless-tested via FakeGateway.
3. **Measurement** (`03`) — finalize the shadow estimator and the measurement envelope; the demo's hero output. (Overlaps with 2; the estimator lives in core.)
4. **Steering — free** (`02`, levers 1–2) — tuned descriptions + static rules starter.
5. **Steering — premium** (`02`, lever 3 / ADR-007) — the dynamic generator. v1 premium.
6. **Context cache** (`04`) — premium anchor; in v1 only if 1–5 are solid and time remains, else first fast-follow (ADR-006).

## v1 (MVP) — what ships
- Foundation + 4–6 free tools + static rules + basic per-call measurement (all free).
- One premium pack: the dynamic steering engine (cache if timeline allows).
- Docs + a 2–3 min demo video showing the **measured** per-call token drop.

## Packaging
- Free MIT core → GitHub (discovery funnel).
- Premium → Gumroad (transactional).
- Plugin-shaped pieces → Fab (secondary; do not gate launch on it).

## Catalog (post-v1, every 4–6 weeks)
Context cache (if deferred) · semantic query packs (lighting / physics / references / naming) · headless test-rig generators · advanced end-to-end measurement.

## The metric that is the moat
Time-to-fix after each UE version bump. The blast radius is contained to `unreal-gateway` by design (ADR-002) — keep it that way.
