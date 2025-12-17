# Fix Docker Compose Command Issue

## Problem
Your VPS has Docker Compose v2 (`docker compose`) but scripts might be using `docker-compose` (v1).

## Solution

### Option 1: Use Docker Compose v2 (Recommended)

Docker Compose v2 uses `docker compose` (space, not hyphen). Update all commands:

**Old (v1):**
```bash
docker-compose up
docker-compose build
docker-compose down
```

**New (v2):**
```bash
docker compose up
docker compose build
docker compose down
```

### Option 2: Install docker-compose v1 (Legacy)

If you need the `docker-compose` command:

```bash
sudo apt update
sudo apt install docker-compose
```

### Option 3: Create Alias (Quick Fix)

Add to `~/.bashrc`:
```bash
alias docker-compose='docker compose'
```

Then reload:
```bash
source ~/.bashrc
```

## Current Status

- ✅ Docker is installed and running
- ✅ Docker Compose v2 is available (`docker compose`)
- ✅ Jenkinsfile updated to use `docker compose`

## Test Commands

```bash
# Test Docker Compose v2
docker compose version

# Test docker-compose.yml
cd /root/idurar-erp-crm
docker compose config

# Run services
docker compose up -d
```

## Jenkinsfile Updated

The Jenkinsfile now uses `docker compose` instead of `docker-compose`.
