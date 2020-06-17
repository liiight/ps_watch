import json
from pathlib import Path
from typing import List

from ps_watch.definitions import default_path
from ps_watch.models import PSItem


def save_item_ids(item_list: List[PSItem], path: Path = default_path):
    items_ids = [item.id for item in item_list]
    path.write_text(json.dumps(items_ids))


def load_item_ids(path: Path = default_path) -> List[str]:
    return json.loads(path.read_text())
