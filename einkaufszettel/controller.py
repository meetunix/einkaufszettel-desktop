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
        self.submit_async_task(self.client.get_ez, self.__set_ez, [eid])

    # callbacks
    def __set_ez(self, ez: str):
        print(ez)

    # async caller
    def submit_async_task(self, method, callback, args: List) -> None:
        try:
            self.executor.submit(method, callback, *args)
        except Exception as e:
            print(e)
