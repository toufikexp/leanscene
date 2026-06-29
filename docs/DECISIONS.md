# Decision records

Short, load-bearing decisions. Read before challenging them; if you still disagree, change the decision here in the same change with rationale.

## ADR-001 — Steer the agent; never mutate the engine as a core mechanism
**Context.** The agent sees both efficient tools and native firehose tools in one registry and will not reliably pick ours. Two ways to force the choice: (a) bias selection with descriptions + rules, (b) deregister/override native tools.
**Decision.** (a) is the mechanism. (b) is fragile against an experimental subsystem and may break per engine bump; it is at most an opt-in flag where the engine cleanly supports it, never the default.
**Consequences.** Steering lives agent-side and survives engine changes. We accept that biasing is probabilistic, so we invest in description quality + rule clarity and measure adherence.
**Do not.** Monkey-patch `ToolsetRegistry`, delete native tools at startup, or depend on internal engine subsystem behavior.

## ADR-002 — Pure core behind a single `UnrealGateway`
**Context.** The UE API is experimental and unavailable in normal CI; logic tested only against a live editor cannot be built reliably by an agent.
**Decision.** All logic is UE-independent and tested headless. The editor sits behind one narrow interface with a real impl and a fixture-backed fake.
**Consequences.** ~80% of the product is ordinary, testable Python. Engine breakage is contained to one package. Cost: capturing fixtures is a manual step and must be kept current.
**Do not.** Import `unreal` anywhere outside `unreal-gateway`. Enforce with an import check in CI.

## ADR-003 — Headline metric is a per-call payload delta, measured, never a fixed %
**Context.** End-to-end savings depend on call count and caching and need a live run; per-call payload reduction is deterministic and free.
**Decision.** Ship the per-call delta as the headline, computed locally with a real tokenizer, always labelled "this call". End-to-end is a separate, opt-in, clearly-labelled premium benchmark.
**Consequences.** Claims stay defensible; no marketing number can be falsified by a skeptical buyer. Cost: the headline is a proxy, and the docs/UI must say so plainly.
**Do not.** Advertise a fixed percentage. Present per-call deltas as workflow savings. Hide the proxy caveat.

## ADR-004 — Open-core split is physical, not conventional
**Context.** Free MIT core funnels adoption; premium is the revenue. They cannot legally or practically mix in the public repo.
**Decision.** Separate trees (`packages/*` free MIT, `premium/*` commercial), with premium extending core through defined extension points. Public repo contains only free trees.
**Consequences.** Premium can be developed/distributed (Gumroad) independently. Cost: extension points must be designed deliberately so premium never needs to fork core.
**Do not.** Put premium code, keys, or licensed logic in the public repo or in any MIT-licensed package.

## ADR-005 — Token-budget by construction
**Decision.** Every tool returns a fixed, minimal schema with bounded size. Unbounded growth with scene size is a design defect, not a tuning problem.
**Consequences.** Predictable cost regardless of scene scale — the core promise. Cost: some queries must summarize/cap/filter rather than return everything.
**Do not.** Return raw lists that scale with actor count; pass through gateway payloads unshaped.

## ADR-006 — Local context cache is the premium anchor and may be a fast-follow
**Context.** The cache is the strongest premium value and the most fragile component (invalidation against live experimental state).
**Decision.** Treat it as the premium anchor. If it threatens the v1 timeline, ship v1 without it and make it the first fast-follow; the dynamic steering engine is the v1 premium in that case.
**Consequences.** v1 can ship on a firm date; the highest-risk code is not on the critical path.
**Do not.** Let cache fragility delay a shippable v1.

## ADR-007 — The dynamic steering engine must be a deterministic generator
**Context.** "Adaptive coordination logic" is too vague to build and risks becoming vaporware.
**Decision.** v1 scope: a generator with explicit inputs (live toolset registry + project manifest) and an explicit output (a tailored ruleset / `CLAUDE.md`), regenerated on toolset change. No runtime ML, no per-prompt rewriting in v1.
**Consequences.** Buildable, testable headless, demonstrable. Cost: less "magic" than the name implies — name it honestly.
**Do not.** Ship something whose behavior cannot be expressed as input→output and tested without a live agent.
