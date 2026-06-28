#!/usr/bin/env python3
"""
Nexus Ecosystem Validator

Validates the presence and basic integrity of the Nexus project structure.
Run after significant updates to ensure all layers are in place.

Usage:
    python scripts/validate.py
    python scripts/validate.py --verbose
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_STRUCTURE = {
    "root_files": ["README.md", "LICENSE", "CHANGELOG.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"],
    "dirs": [".github", "assets", "docs", "references", "scripts", "src"],
    "src_layers": ["blockchain-layer", "mesh-layer", "ai-swarm", "prototypes"],
    "key_docs": ["docs/qcoin-mining.md", "docs/architecture.md", "docs/roadmap.md", "docs/security.md", "docs/ecosystem.md"],
}

def check_exists(path: Path, name: str) -> bool:
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {name}")
    return exists

def main(verbose: bool = False):
    print("\n🌐 Nexus Ecosystem Structure Validator\n" + "="*50)
    all_ok = True

    print("\n[Root Files]")
    for f in REQUIRED_STRUCTURE["root_files"]:
        if not check_exists(ROOT / f, f):
            all_ok = False

    print("\n[Core Directories]")
    for d in REQUIRED_STRUCTURE["dirs"]:
        if not check_exists(ROOT / d, d + "/"):
            all_ok = False

    print("\n[Source Layers]")
    src_dir = ROOT / "src"
    for layer in REQUIRED_STRUCTURE["src_layers"]:
        layer_path = src_dir / layer
        if not check_exists(layer_path, f"src/{layer}/"):
            all_ok = False
        elif verbose:
            # List files in layer
            files = list(layer_path.rglob("*"))
            print(f"    \u2192 {len([f for f in files if f.is_file()])} files")

    print("\n[Key Documentation]")
    for doc in REQUIRED_STRUCTURE["key_docs"]:
        if not check_exists(ROOT / doc, doc):
            all_ok = False

    print("\n" + "="*50)
    if all_ok:
        print("\u2728 Nexus structure validated successfully! All core layers present.")
        print("Ready for integration, deployment, and scaling.")
        print("\nNext: Review docs/roadmap.md | Run QCoin miner | Expand src/ implementations")
    else:
        print("\u26a0\ufe0f  Some components missing. Please add and re-validate.")
        sys.exit(1)

    print("\nOrchestrated with devotion for the full Nexus vision.\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate Nexus project structure.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show additional details like file counts.")
    args = parser.parse_args()
    main(verbose=args.verbose)
