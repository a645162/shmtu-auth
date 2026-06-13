# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

上海海事大学校园网自动认证工具 (SHMTU Campus Network Auto Authentication Tool). Automatically detects network authentication status and performs login when offline.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the authentication monitor
python -m shmtu_auth

# Run with custom config path
python -m shmtu_auth -t /path/to/config.toml

# Lint with ruff
ruff check .

# Lint with flake8
flake8 .

# Docker (headless version for servers)
docker compose -f docker_headless/docker-compose.yml up --build -d
```

## Architecture

### Two Entry Points

1. **Main Application** (`src/shmtu_auth/`): Full-featured CLI/GUI application
   - Entry: `src/shmtu_auth/__main__.py` → `src/shmtu_auth/src/entry.py`
   - Dependencies: requests, loguru, toml, PyYAML, chardet

2. **Docker Headless** (`docker_headless/app/`): Minimal dependency version for servers
   - Entry: `docker_headless/app/main.py`
   - Dependencies: only requests (no loguru, toml, PyQt)
   - Logs to stdout for Docker compatibility

### Core Authentication Flow

```
src/shmtu_auth/src/core/
├── core.py              # ShmtuNetAuthCore - main auth logic with dual login strategy
├── core_exp.py          # Network connectivity check and query string extraction
├── get_query_string_requests.py  # HTTP probes to detect auth portal
├── shmtu_auth.py        # ShmtuNetAuth - wrapper with user list iteration
└── shmtu_auth_const_value.py  # Service type constants
```

**Dual Login Strategy** (in `core.py`):
1. First attempt: Legacy eportal login (`ismu.shmtu.edu.cn:8443/eportal/`)
2. Fallback: H3C Portal login (`hwifi.shmtu.edu.cn/portalauth/login`)

The H3C fallback handles cases where the campus network uses a different portal system.

### Configuration Priority

Config values are resolved in this order (see `src/shmtu_auth/src/utils/env.py`):
1. Global config (`config_global.py`)
2. TOML config file (`config.toml`)
3. Environment variables

### Key Environment Variables

```bash
SHMTU_AUTH_USER_LIST=202540510004;202540510005  # Semicolon-separated user IDs
SHMTU_AUTH_USER_PWD_<学号>=password             # Password per user ID
SHMTU_AUTH_TIME_INTERVAL=60                     # Check interval in seconds
```

### Monitor Loop

`src/shmtu_auth/src/monitor/auth_status.py`:
- Runs in a background thread
- Periodically checks connectivity via Baidu/Bilibili probes
- Attempts login for each configured user until one succeeds

## Docker Headless

The `docker_headless/` directory is a standalone minimal version:
- No GUI dependencies
- No loguru/toml/PyQt dependencies
- Same dual login strategy (legacy + H3C fallback)
- Environment variable configuration only

## Testing

Test files are in `PyTest/`. SSL-related tests in `PyTest/SSL/` for handling certificate issues.
