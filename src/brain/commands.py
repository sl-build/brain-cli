"""Brain CLI v2 — Command handlers (think, key, key-set)."""

from __future__ import annotations

import sys

from .client import call_and_print
from .context import build_context_block
from .errors import InputError
from .keys import get_api_key, set_api_key, find_key_source, PROFILE_ENV, VALID_PROVIDERS
from .profiles import VALID_PROFILES, PROFILE_PROMPTS
from .depth import VALID_DEPTHS
from .config import load_config, save_config, get_default_provider, get_default_model as get_config_model


def cmd_think(
    prompt: str,
    *,
    model: str | None = None,
    provider: str | None = None,
    profile: str | None = None,
    context: str | None = None,
    context_file: str | None = None,
    stdin_context: bool = False,
    metadata: list[str] | None = None,
    depth: str | None = None,
    max_tokens: int = 16384,
    temperature: float | None = None,
    raw: bool = False,
    json_output: bool = False,
    show_stats: bool = False,
) -> str:
    """Handle the 'think' subcommand."""
    if profile and profile not in VALID_PROFILES:
        raise InputError(f"Unknown profile: {profile}. Valid: {', '.join(VALID_PROFILES)}")

    if depth and depth not in VALID_DEPTHS:
        raise InputError(f"Unknown depth: {depth}. Valid: {', '.join(VALID_DEPTHS)}")

    # Resolve provider and model from config if not given
    provider = provider or get_default_provider()
    if model is None:
        model = get_config_model()

    context_block = build_context_block(
        context=context,
        context_file=context_file,
        stdin_context=stdin_context,
        metadata=metadata,
    )

    return call_and_print(
        prompt=prompt,
        model=model,
        provider=provider,
        context_block=context_block,
        depth=depth,
        max_tokens=max_tokens,
        temperature=temperature,
        profile=profile,
        raw=raw,
        json_output=json_output,
        show_stats=show_stats,
    )


def cmd_key() -> None:
    """Handle the 'key' subcommand — show key location and masked value."""
    config = load_config()
    source = find_key_source(config["provider"])
    if source is None:
        print("No key found. Use: brain key-set <key_value>")
        print("Or set interactively: brain think \"hello\"")
        print(f"Or edit: {PROFILE_ENV}")
        return

    key, path = source
    if len(key) > 12:
        masked = key[:8] + "..." + key[-4:]
    else:
        masked = "***"

    if path:
        print(f"Found in {path}: {masked}")
    else:
        print(f"Found in env var: {masked}")


def cmd_key_set(key_value: str) -> None:
    """Handle the 'key-set' subcommand — save API key."""
    key_value = key_value.strip()
    if not key_value:
        print("Empty key. Aborting.", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    path = set_api_key(key_value, provider=config["provider"])
    print(f"Key saved to {path}")


def cmd_profiles() -> str:
    """List available reasoning profiles."""
    lines = ["Available reasoning profiles:", ""]
    for name, cfg in PROFILE_PROMPTS.items():
        lines.append(f"  {name}: depth={cfg['default_depth']}, temp={cfg['default_temperature']}")
        lines.append(f"    {cfg['system_prompt'][:80]}...")
    result = "\n".join(lines)
    print(result)
    return result


def cmd_config() -> None:
    """Show current configuration."""
    config = load_config()
    print(f"provider: {config['provider']}")
    model = config["model"]
    print(f"model: {model if model else '(provider default)'}")


def cmd_config_set(key: str, value: str) -> None:
    """Set a configuration value."""
    if key not in ("provider", "model"):
        raise InputError(f"Unknown config key: {key}. Valid: provider, model")

    if key == "provider" and value not in VALID_PROVIDERS:
        raise InputError(f"Unknown provider: {value}. Valid: {', '.join(VALID_PROVIDERS)}")

    save_config(key, value)
    print(f"Set {key} = {value if value else '(empty)'}")
