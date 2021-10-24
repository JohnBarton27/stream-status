import requests
from requests.auth import HTTPBasicAuth

from streamstatus.application import Application


class PTZCam(Application):

    def __init__(self, hostname: str, port: int = 80, app_name: str = None):
        super().__init__(hostname, port, app_name=app_name)

    @property
    def is_up(self):
        try:
            response = requests.get(self.url, timeout=5, auth=HTTPBasicAuth('admin', 'admin'))
        except OSError:
            return False

        return response.status_code in [200, 401]

    def _get_app_name(self):
        return 'NDI'
