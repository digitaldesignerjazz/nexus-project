# Nexus Scripts

Automation, monitoring, deployment, and validation tools for the Nexus ecosystem.

## Purpose
- Mesh network status checks, peer management, and restarts (Yggdrasil, Tenda, Docker)
- AI agent heartbeat monitors, swarm orchestration helpers, and self-improvement triggers
- Blockchain queries, QCoin balance/chain validation, mining helpers
- Prototype control scripts and hardware interface tests
- Overall Nexus health validation and reporting

## Usage
Run scripts from project root or integrate into Docker/CI.

Example:
```bash
python scripts/validate.py
python scripts/nexus-monitor.py --layer all
```

## Guidelines
- Keep scripts modular, well-documented, and idempotent where possible.
- Support both simulation and live modes.
- Log outputs for monitoring dashboards.
- Future: integrate with Grok Launcher for visual status.

*Part of the living Nexus orchestrator — evolving with the stack.*