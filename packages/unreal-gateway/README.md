# leanscene-unreal-gateway (free, MIT)

The **only** tree allowed to import `unreal` (ADR-002). Everything else is pure
logic behind the `UnrealGateway` interface.

- **`FakeGateway`** — serves hand-written seed fixtures from `tests/fixtures/`.
  Lets every other package be tested headless (no editor, no network).
- **`RealGateway`** — the Web Remote Control implementation. Currently a **stub**:
  signatures + TODOs only. The experimental UE 5.8 payload shapes are not guessed
  from memory; they must be verified against a live editor. Real round-trip tests
  are `@pytest.mark.editor` and run manually (excluded from default CI).

When UE bumps versions, this package is where the break is contained.
