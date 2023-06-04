import dataclasses
import json
import uuid
from dataclasses import dataclass
from typing import List


@dataclass
class Server:
    name: str
    base_url: str
    port: int
    descr: str = "n.a."
    username: str = None  # credentials for optional http basic auth
    password: str = None


@dataclass
class Configuration:
    servers: List[Server]
    version: int


@dataclass
class Item:
    iid: uuid
    itemName: str
    ordinal: int
    amount: int
    size: float
    unit: str
    catDescription: str
    catColor: str


@dataclass
class Einkaufszettel:
    eid: uuid
    created: int
    modified: int
    name: str
    version: int
    items: List[Item]

    def get_json(self):
        return json.dumps(dataclasses.asdict(self), sort_keys=True, indent=4)

    def get_dict(self):
        return dataclasses.asdict(self)
