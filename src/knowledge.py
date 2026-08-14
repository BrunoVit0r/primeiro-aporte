from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_knowledge(data_dir: Path) -> list[dict[str, Any]]:
    with (data_dir / "base_educacional.json").open(encoding="utf-8") as file:
        topics = json.load(file)
    if not isinstance(topics, list) or not topics:
        raise ValueError("A base educacional precisa conter uma lista de tópicos.")
    return topics
