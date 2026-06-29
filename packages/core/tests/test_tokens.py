"""Token meter: stable offline counts + tokenizer-agnostic wiring (ADR-003)."""
from leanscene_core import TiktokenCounter, TokenMeter


def test_offline_tiktoken_counts_are_stable():
    meter = TokenMeter()  # default offline proxy, vendored encoding, no network
    # cl100k_base, deterministic and fixed:
    assert meter.count_tokens("") == 0
    assert meter.count_tokens("hello world") == 2
    assert meter.count_tokens("The quick brown fox jumps over the lazy dog.") == 10
    # determinism across repeated calls
    assert meter.count_tokens("hello world") == meter.count_tokens("hello world")


def test_count_bytes_matches_count_tokens():
    meter = TokenMeter()
    text = "hello world"
    assert meter.count_bytes(text.encode("utf-8")) == meter.count_tokens(text)


def test_meter_is_tokenizer_agnostic_via_injected_counter():
    class WordCounter:
        def count(self, text: str) -> int:
            return len(text.split())

    meter = TokenMeter(counter=WordCounter())
    assert meter.count_tokens("a b c") == 3


def test_tiktoken_counter_uses_named_encoding_offline():
    counter = TiktokenCounter()  # default cl100k_base, vendored cache
    assert counter.encoding_name == "cl100k_base"
    assert counter.count("hello world") == 2
