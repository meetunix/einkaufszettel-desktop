import uuid

import requests

from einkaufszettel.entities import Server


class EinkaufszettelRestClient:
    """
    This class provides methods (executed as asynchronous jobs by the controller) for communication with the
    einkaufszettel-server.

    This class holds a requests-session object, that is used for all requests.
    """
    def __init__(self, server: Server):
        self.session = requests.Session()
        self.server = server
        self.put_headers = {"Content-Type": "application/json"}
        self.get_headers = {"Accept": "application/json"}

    def get_ez(self, eid: str) -> str:
        url = f"{self.server.base_url}:{self.server.port}/r0/ez/{eid}"

        r = self.session.get(url, headers=self.get_headers, timeout=2)
        print(f"response: {r.status_code} -> {r.text}")
        r.raise_for_status()
        return r.text
