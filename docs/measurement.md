# Measurement (honest, by construction)

LeanScene's headline number is a **per-call payload token delta**, computed locally
with a real tokenizer (ADR-003). This doc says exactly what it is — and what it is
not — so the number can never be oversold.

## What the per-call delta is
For a single lean tool call, the estimator counts:
- `lean_tokens` — the tokens in the lean result the agent actually receives.
- `firehose_tokens` — the tokens in the native payload it would otherwise have
  pulled for the equivalent query.
- `delta_pct_this_call` — the reduction, **for that one call**.

It is deterministic, offline, and instant. Every tool result carries it in a
`measure` block; the field name keeps the `this_call` label so the framing travels
with the number.

## What it is NOT
- It is **not** end-to-end workflow savings. Real workflow savings depend on how
  many calls happen and on caching across a session — that is a separate, premium
  benchmark (`EndToEndResult` / `EndToEndBenchmark`), reported with its own
  `kind = "end_to_end"` and field names that cannot be confused with the per-call
  delta.
- It is **not** a fixed advertised percentage. There is no constant saving claim
  anywhere in this repo (a test enforces that). Every number is computed from the
  two payloads in front of it, per call.

## Seeing it
Run the demo against the seed scenes:

```
python demo/measure_demo.py
```

It prints a per-call-labelled report (tool, scene, lean, firehose, delta — this
call). ⚠️ On the seed fixtures the firehose payloads are **synthetic**, so the
absolute deltas are illustrative until real Web Remote Control captures replace
them (`docs/capturing-fixtures.md`). The mechanism is real and offline; the inputs
are placeholders.

## The line we hold
Per-call payload delta = free, deterministic, honest proxy (this call only).
End-to-end workflow savings = separate, premium, clearly labelled, never conflated.
