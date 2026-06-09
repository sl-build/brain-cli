"""Brain CLI v2 — Persistent config file support."""

from __future__ import annotations

from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "brain"
CONFIG_FILE = CONFIG_DIR / "config.toml"


def _ensure_config() -> None:
    """Ensure config directory and file exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(
            '[defaults]\nprovider = "openrouter"\nmodel = ""\n'
        )


def load_config() -> dict:
    """Read config file, return dict with provider and model."""
    import tomllib

    _ensure_config()
    data = CONFIG_FILE.read_text()
    parsed = tomllib.loads(data)
    defaults = parsed.get("defaults", {})
    return {
        "provider": defaults.get("provider", "openrouter"),
        "model": defaults.get("model", ""),
    }


def save_config(key: str, value: str) -> None:
    """Update a config key and save the file."""
    if key not in ("provider", "model"):
        raise ValueError(f"Invalid config key: {key}")
    _ensure_config()
    config = load_config()
    config[key] = value

    lines = ["[defaults]"]
    for k, v in config.items():
        if v == "":
            lines.append(f'{k} = ""')
        else:
            lines.append(f'{k} = "{v}"')
    CONFIG_FILE.write_text("\n".join(lines) + "\n")


def get_default_provider() -> str:
    """Return the default provider from config."""
    return load_config()["provider"]


def get_default_model() -> str | None:
    """Return the default model from config, or None if empty."""
    model = load_config()["model"]
    return model if model else None
