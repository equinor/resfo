from dataclasses import dataclass
from typing import Any


@dataclass
class Record:
    keyword: str
    values: Any
