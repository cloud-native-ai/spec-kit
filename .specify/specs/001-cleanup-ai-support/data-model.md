# Data Model: Agent Configuration

## Agent Registry Schema

The core configuration dictionary `AGENT_CONFIG` restricts allowed AI providers.

```python
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
}
```

## Field Definitions

| Field | Type | Description |
|---|---|---|
| key | str | CLI argument key (e.g. `copilot`) |
| name | str | Display name for UI |
| folder | str | Configuration directory name (e.g. `.github/`) |
| install_url | str? | URL to install CLI tool if required |
| requires_cli | bool | Whether to check for binary existence |

All other keys found in previous versions (`claude`, `gemini`, etc.) must be removed alongside their associated logic.
