import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from einkaufszettel.client import EinkaufszettelRestClient
from einkaufszettel.entities import Einkaufszettel, Server, Configuration


class Controller:

    def __init__(self, config_path: str = "~/.config/ezrc.json"):
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.__load_config(config_path)
        self.client = EinkaufszettelRestClient(self.configuration.get_default_server())

    def __load_config(self, path: str) -> None:
        """Load configuration object from file (default: ~/.config/ezrc.json)."""
        path = Path(path).expanduser()
        if not path.is_file():
            pass  # TODO execute config window for creating initial config
        self.configuration = Configuration.from_json(json.loads(path.read_text()))

    def get_configuration(self, path: str, force_reload: bool = False) -> Configuration:
        if force_reload or self.configuration is None:
            self.__load_config(path)
        return self.configuration

    def set_server(self, server: Server) -> None:
        self.client = EinkaufszettelRestClient(server)

    def get_ez(self, eid: str, callback) -> None:
        print("get_ez")
        self.submit_async_task(self.__fetch_and_set_ez, eid, callback)

    # callbacks
    def __fetch_and_set_ez(self, eid: str, callback) -> None:
        try:
            response = self.client.get_ez(eid)
        except Exception as e:
            print(e)
            return

        ez = Einkaufszettel.from_json(json.loads(response))
        callback(ez) # TODO: execute callable here

    # async caller
    def submit_async_task(self, method, *args) -> None:
        print("submit_async_task")
        self.executor.submit(method, *args)
