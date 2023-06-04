import uuid

import requests

from einkaufszettel.entities import Server


class EinkaufszettelRestClient:
    """
    This class provides methods (executed as asynchronous jobs by the controller) for communication with the
    einkaufszettel-server.

    This class holds a requests-session object, that is used for all requests.
    """

    # TODO: configure base_path from config file

    def __init__(self, server: Server):
        self.session = requests.Session()
        self.server = Server

    def get_ez(self, eid: uuid) -> str:
        url = f"{self.server.base_url}/r0/ez/{eid}"

        r = self.session.get(url, timeout=5)
        r.raise_for_status()
        return r.text
