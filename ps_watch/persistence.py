import json
from pathlib import Path
from typing import List

from ps_watch.definitions import default_path
from ps_watch.models import PSItem


def save_items(item_list: List[PSItem], path: Path = default_path):
    path.write_text(json.dumps([item.json() for item in item_list]))


def load_items(path: Path = default_path) -> List[PSItem]:
    return [PSItem.parse_obj(item) for item in json.loads(path.read_text())]
