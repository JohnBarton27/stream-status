import requests

from streamstatus.application import Application


class TallyArbiter(Application):

    def __init__(self, hostname: str, port: int = 4455, app_name: str = None):
        super().__init__(hostname, port, app_name=app_name)

    def _get_app_name(self):
        return 'Tally Arbiter'
