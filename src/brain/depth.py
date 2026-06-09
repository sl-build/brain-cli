"""Brain CLI v2 — Depth presets mapping to model parameters."""

from __future__ import annotations

DEPTH_CONFIGS: dict[str, dict] = {
    "quick": {
        "max_output_tokens": 2048,
        "temperature": 0.2,
        "reasoning_effort": "low",
    },
    "normal": {
        "max_output_tokens": 8192,
        "temperature": 0.3,
        "reasoning_effort": "medium",
    },
    "deep": {
        "max_output_tokens": 16384,
        "temperature": 0.4,
        "reasoning_effort": "high",
    },
    "exhaustive": {
        "max_output_tokens": 32768,
        "temperature": 0.5,
        "reasoning_effort": "high",
    },
}

VALID_DEPTHS = list(DEPTH_CONFIGS.keys())

DEFAULT_DEPTH = "normal"


def get_depth_config(depth: str) -> dict:
    """Return merged config for a depth level."""
    if depth not in DEPTH_CONFIGS:
        raise ValueError(f"Unknown depth: {depth}. Valid: {VALID_DEPTHS}")
    return DEPTH_CONFIGS[depth].copy()


def merge_depth_into_params(
    params: dict,
    depth: str,
    max_tokens_override: int | None = None,
    temperature_override: float | None = None,
) -> dict:
    """Merge depth preset into API call params.

    Explicit --max-tokens and --temperature override depth defaults.
    """
    cfg = get_depth_config(depth)
    merged = params.copy()

    # Depth-provided defaults
    if "max_tokens" not in merged:
        merged["max_tokens"] = cfg["max_output_tokens"]
    if "temperature" not in merged:
        merged["temperature"] = cfg["temperature"]

    # Reasoning effort: only set if model supports it (OpenAI o-series)
    if cfg.get("reasoning_effort"):
        merged["reasoning_effort"] = cfg["reasoning_effort"]

    # Explicit overrides win over everything
    if max_tokens_override is not None:
        merged["max_tokens"] = max_tokens_override
    if temperature_override is not None:
        merged["temperature"] = temperature_override

    return merged