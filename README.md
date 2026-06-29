# LeanScene

Cut your AI agent's token cost in large Unreal Engine scenes — and prove the saving with local, no-API measurement.

## The problem
When an AI agent (Claude Code, Cursor) works inside a large UE 5.8 scene over MCP, naive reads of the outliner / actor list / asset state blow up the context window, burn tokens, and degrade accuracy. Epic's native tools connect the agent but return the full firehose.

## What LeanScene does
1. **Token-efficient MCP tools** — spatial/semantic queries and compact serializers that return only task-relevant data.
2. **Agent steering** — tool descriptions + rules that get the agent to actually use the efficient tools instead of the firehose.
3. **Local measurement** — every lean call reports the per-call token delta vs. the equivalent native query, computed locally with a real tokenizer. No API calls, no guesswork.

## Open-core
- **Free (MIT):** the full tool library, the static rules starter, the basic per-call measurement.
- **Premium:** the dynamic steering engine, the local context cache (compounding savings across a session), and end-to-end benchmarking. → Gumroad.

## Status
Experimental, tracking UE 5.8's experimental MCP + Web Remote Control APIs. Expect breakage across engine versions; maintenance velocity is the point.

## Docs
See `docs/ARCHITECTURE.md` and `docs/ROADMAP.md`.

## License
Core: MIT. Premium packs: separate commercial license.
