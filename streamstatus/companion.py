import requests

from streamstatus.application import Application


class Companion(Application):

    def __init__(self, hostname: str, port: int = 8000):
        super().__init__(hostname, port)

    @property
    def app_name(self):
        return 'Companion'

    @property
    def is_up(self):
        try:
            response = requests.get(self.url, timeout=5)
        except OSError:
            return False

        return response.status_code == 200
