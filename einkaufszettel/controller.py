import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from einkaufszettel.client import EinkaufszettelRestClient
from einkaufszettel.entities import Einkaufszettel, Server, Configuration, ConfigEZ


class Controller:
    def __init__(self, config_path: Path, cache_path: Path):
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.__load_config(config_path)
        self.cache_path = cache_path
        self.config_path = config_path
        self.client = EinkaufszettelRestClient(self.configuration.get_default_server())
        # todo check if config and cache dir are accessible, otherwise throw error

    def __load_config(self, path: Path) -> None:
        """Load configuration object from file (default: ~/.config/ezrc.json)."""
        path = path.expanduser()
        if not path.is_file():
            pass  # TODO execute config window for creating initial config
        self.configuration = Configuration.from_json(json.loads(path.read_text()))

    def get_configuration(self, force_reload: bool = False) -> Configuration:
        if force_reload or self.configuration is None:
            self.__load_config(self.config_path)
        return self.configuration

    def get_default_ez_from_cache(self) -> Einkaufszettel:
        config_ez = self.configuration.get_default_ez()
        return self.get_ez_from_cache(config_ez.eid)

    def set_server(self, server: Server) -> None:
        self.client.set_server = server

    def get_ez_from_remote(self, eid: str, callback) -> None:
        print("get_ez")
        self.submit_async_task(self.__fetch_and_set_ez, eid, callback)

    def get_ez_from_cache(self, eid: str) -> Einkaufszettel:
        path = self.cache_path / Path(f"{eid}.json")
        return Einkaufszettel.from_json(json.loads(path.read_text()))

    def get_all_ez_from_config(self) -> List[ConfigEZ]:
        return sorted(list(self.configuration.ezs), key=lambda x: x.name)

    # callbacks
    def __fetch_and_set_ez(self, eid: str, callback, *args) -> None:
        try:
            response = self.client.get_ez(eid)
        except Exception as e:
            print(e)
            return

        ez = Einkaufszettel.from_json(json.loads(response))
        callback(ez)  # TODO: execute callable here

    # async caller
    def submit_async_task(self, method, *args) -> None:
        self.executor.submit(method, *args)
