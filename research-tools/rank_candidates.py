"""Print the current public-source ranking as JSON.

Run from the repository root:
    python3 research-tools/rank_candidates.py
"""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path(__file__).with_name("candidate_registry.json")
MODULE_PATH = ROOT / "demo-api-hpc" / "candidate_ranking.py"


def load_ranker():
    spec = importlib.util.spec_from_file_location("candidate_ranking", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ranked = load_ranker().rank_candidates(registry["candidates"])
    print(json.dumps({"registry_date": registry["registry_date"], "ranked_candidates": ranked}, indent=2))


if __name__ == "__main__":
    main()
