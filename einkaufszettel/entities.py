import dataclasses
import json
import uuid
from dataclasses import dataclass
from typing import List, Set

from einkaufszettel.exceptions import EZConfigurationException


@dataclass
class ExportBase:
    def get_json(self):
        return json.dumps(dataclasses.asdict(self), sort_keys=True, indent=4)

    def get_dict(self):
        return dataclasses.asdict(self)


@dataclass
class Server:
    id: int
    name: str
    base_url: str
    port: int
    descr: str = "n.a."
    username: str = None  # credentials for optional http basic auth
    password: str = None

    def __hash__(self):
        return hash((self.id, self.name, self.base_url, self.port, self.descr, self.username, self.password))


@dataclass
class ConfigEZ:
    eid: str
    name: str
    server_id: int  # the server where the ez belongs to

    # used by the ttk.listbox widget
    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.eid)


@dataclass
class Configuration(ExportBase):
    version: int
    default_server_id: int
    default_eid: str
    ezs: Set[ConfigEZ]
    servers: Set[Server]

    @staticmethod
    def from_json(json_conf: json):
        json_conf["servers"] = {Server(**s) for s in json_conf["servers"]}
        json_conf["ezs"] = {ConfigEZ(**ez) for ez in json_conf["ezs"]}
        return Configuration(**json_conf)

    def get_default_server(self) -> Server:
        return self.get_server_by_id(self.default_server_id)

    def get_server_by_id(self, id: int) -> Server:
        for server in self.servers:
            if server.id == id:
                return server
        raise EZConfigurationException(f"The server with the default server id {self.default_server_id} does not exists.")

    def set_default_server(self, server: Server) -> None:
        self.add_new_server(server)
        self.default_server_id = server.id

    def add_new_server(self, server: Server) -> None:
        max_server_id = 1
        for s in self.servers:
            if server.id > max_server_id:
                max_server_id = server.id

        server.id = max_server_id + 1
        self.servers.add(server)

    def get_default_ez(self) -> ConfigEZ:
        for ez in self.ezs:
            if ez.eid == self.default_eid:
                return ez
        raise EZConfigurationException(
            f"The Einkaufszettel with the default id {self.default_eid} does not exist in configuration."
        )

    def set_default_ez(self, ez: ConfigEZ) -> None:
        self.add_new_ez(ez)
        self.default_eid = ez.eid

    def add_new_ez(self, ez: ConfigEZ) -> None:
        self.ezs.add(ez)


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
class Einkaufszettel(ExportBase):
    eid: uuid
    created: int
    modified: int
    name: str
    version: int
    items: List[Item]

    def get_json(self):
        return json.dumps(dataclasses.asdict(self), sort_keys=True)

    @staticmethod
    def from_json(json_ez: json):
        json_ez["items"] = [Item(**item) for item in json_ez["items"]]
        return Einkaufszettel(**json_ez)
