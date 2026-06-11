# Brain Hermes Plugin (optional, experimental)

> **Version:** matches brain-cli (currently v0.2.0)
> **Not included in the brain pip package.** Installed separately via Hermes Agent.

## Installation

```bash
Copy plugin.yaml to the Hermes agent skills directory
cp plugin/brain-tool/plugin.yaml ~/.hermes/skills/
```

## Plugin tools

| Tool | Purpose |
|-----------|------------|
| `brain_think` | Run reasoning via Brain CLI |
| `brain_config` | Manage configuration |
| `brain_plan` | Plan management (show/mark/block) |
| `brain_plan_status` | Brain Gate status |

## Brain Gate

Gate protects against cyclic calls. It blocks `brain think` if brain itself called an agent that called brain. See `brain plan --block` / `--mark-done`.

## Dependencies

- brain CLI v0.2.0+ (`pip install brain`)
- Hermes Agent
