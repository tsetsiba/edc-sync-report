import requests
from requests.exceptions import ConnectionError


class SyncConnectionError(Exception):
    pass


class FetchSyncData:
    """A class to fetch sync report data from a registered
    site remotely.
    """

    def __init__(self, site, *args, **kwargs):
        self.site = site

    def data(self):
        try:
            request = requests.get(self.site.remote_url, timeout=1)
            return request.json()
        except ConnectionError as e:
            raise SyncConnectionError(f'{e}') from e
