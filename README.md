# Brain CLI v0.2.0 — Reasoning Engine for AI Agents

[![PyPI version](https://img.shields.io/pypi/v/brain)](https://pypi.org/project/brain/)

Brain CLI is an exocortex for AI agents. It sends prompts to reasoning models (OpenAI, Anthropic, Gemini, DeepSeek, Qwen) via OpenRouter and returns the response. Can be used as an MCP tool or standalone.

## Quick Start

```bash
pip install brain
export OPENROUTER_API_KEY=sk-or-...
brain think "How does async/await work in Python?"
```

## Usage

- `brain think "prompt"` — basic
- `brain think "prompt" --model gpt-4o --depth high` — with model and depth
- `brain think "prompt" --context "context"` — with context
- `brain think "prompt" --context-file file.txt` — from file
- `cat log.txt | brain think "why?" --stdin-context` — from stdin
- `brain think "prompt" --json` — JSON response
- `brain think "prompt" --stats` — with stats
- `brain think "prompt" --plan` — planning mode
- `brain think "prompt" --session-id my-session` — multi-session

## Plan Management

- `brain plan` — show plan
- `brain plan --mark-done` — mark step done
- `brain plan --block` — block step

## Provider

Default is OpenRouter (300+ models). Can be switched:

```bash
brain config-set --provider opencode_go
brain config-set --provider openrouter
```

## Profiles

Six built-in profiles: reasoning, writer, planner, critic, research, creative.

Custom profiles:

```bash
brain profile-add my-profile template=reasoning model=qwen-max-0125
brain profiles
brain profile-remove my-profile
```

## Depth presets

- `low` — fast, shallow
- `medium` (default) — balanced
- `high` — deep reasoning

## Hermes Plugin (optional, experimental)

Brain CLI can be connected to a Hermes agent. See plugin/README.md.

Note: not included in the pip package; installed separately.

## Install

```bash
pip install brain
```

For Hermes Agent: `pip install brain hermes` (plugin not included, see plugin/README.md)

## Requirements

Python 3.11+, API key from OpenRouter (openrouter.ai/keys)

## License

MIT
