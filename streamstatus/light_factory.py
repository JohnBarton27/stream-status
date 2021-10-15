import requests

from streamstatus.application import Application


class LightFactory(Application):

    def __init__(self, hostname: str, port: int = 80, app_name: str = None):
        super().__init__(hostname, port, app_name=app_name)

    def _get_app_name(self):
        return 'Light Factory'
