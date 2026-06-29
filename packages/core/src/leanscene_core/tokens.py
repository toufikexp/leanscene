"""Token meter — local, offline, deterministic token counting.

ADR-003: the headline metric is a per-call payload token delta computed locally
with a real tokenizer. This module is that tokenizer wiring. It is pure and
offline: the default backend uses a *vendored* tiktoken encoding, so there is no
network access at import or call time.

Honesty note (ADR-003): the offline backend is a PROXY tokenizer. Its counts are
real, deterministic and free, but they are not Anthropic's exact tokenization.
Exact Claude counts require Anthropic's networked count-tokens API, which would
break the offline guarantee — see ``AnthropicTokenCounter`` (a deliberate stub).
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable

#: Vendored tiktoken cache dir holding the pre-fetched encoding blob, so the
#: default counter loads with no network. The blob is the sha1-named cache file
#: tiktoken expects; it was fetched once at build time (see project docs).
VENDORED_TIKTOKEN_CACHE = Path(__file__).parent / "_vendor" / "tiktoken_cache"

#: Default proxy encoding. Swappable; documented as a proxy, not Claude-exact.
DEFAULT_ENCODING = "cl100k_base"


@runtime_checkable
class TokenCounter(Protocol):
    """Anything that turns text into a token count."""

    def count(self, text: str) -> int:
        ...


@contextmanager
def _tiktoken_cache_dir(cache_dir: Path):
    """Point tiktoken at a specific offline cache dir for the duration of a load,
    without permanently mutating the process environment."""
    key = "TIKTOKEN_CACHE_DIR"
    prev = os.environ.get(key)
    os.environ[key] = str(cache_dir)
    try:
        yield
    finally:
        if prev is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = prev


class TiktokenCounter:
    """Offline tiktoken-backed counter.

    Loads a *vendored* encoding so it works with no network. This is the default
    proxy tokenizer (ADR-003).
    """

    def __init__(
        self,
        encoding_name: str = DEFAULT_ENCODING,
        cache_dir: Path = VENDORED_TIKTOKEN_CACHE,
    ) -> None:
        import tiktoken  # lazy: importing this module must not require tiktoken

        self.encoding_name = encoding_name
        with _tiktoken_cache_dir(cache_dir):
            self._enc = tiktoken.get_encoding(encoding_name)

    def count(self, text: str) -> int:
        return len(self._enc.encode(text))


class AnthropicTokenCounter:
    """STUB — exact Anthropic/Claude token counting.

    Anthropic's count-tokens is a NETWORK API call, which violates the offline
    guarantee (ADR-003) and is exactly the kind of unstable surface we do not
    guess from memory (project instructions). It is left as a deliberate stub
    with a manual wiring TODO and is never part of the default offline path.

    TODO(manual, needs network + an API key): wire to Anthropic's count-tokens
    endpoint behind an explicit opt-in, keep it OUT of default headless CI, and
    label any number it produces as exact-but-networked vs. the offline proxy.
    """

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "AnthropicTokenCounter is a stub: exact Claude token counting needs a "
            "network API call and is intentionally not implemented offline. Use "
            "TiktokenCounter for the offline proxy count (ADR-003)."
        )

    def count(self, text: str) -> int:  # pragma: no cover - stub
        raise NotImplementedError


class TokenMeter:
    """Pure function object: text/bytes -> token count, via a pluggable counter.

    Defaults to the offline tiktoken proxy. Inject any ``TokenCounter`` — e.g. a
    deterministic fake in tests, or a networked exact counter when opted in.
    """

    def __init__(self, counter: Optional[TokenCounter] = None) -> None:
        self._counter = counter if counter is not None else TiktokenCounter()

    @property
    def counter(self) -> TokenCounter:
        return self._counter

    def count_tokens(self, text: str) -> int:
        return self._counter.count(text)

    def count_bytes(self, data: bytes, encoding: str = "utf-8") -> int:
        return self._counter.count(data.decode(encoding))
