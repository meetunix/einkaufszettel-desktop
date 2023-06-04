from concurrent.futures import ThreadPoolExecutor
from typing import List

from einkaufszettel.client import EinkaufszettelRestClient
from einkaufszettel.entities import Einkaufszettel, Server


class Controller:

    def __init__(self, server: Server):
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.client = EinkaufszettelRestClient(server)
        pass

    def set_server(self, server: Server) -> None:
        self.client = EinkaufszettelRestClient(server)

    def get_ez(self, eid: str) -> None:
        print("get_ez")
        self.submit_async_task(self.__fetch_and_set_ez, eid)

    # callbacks
    def __fetch_and_set_ez(self, eid: str) -> None:
        try:
            response = self.client.get_ez(eid)
        except Exception as e:
            print(e)
            return

        print("callable is executed here -> " + response)

    # async caller
    def submit_async_task(self, method, *args) -> None:
        print("submit_async_task")
        self.executor.submit(method, *args)
