from configparser import ConfigParser
from datetime import datetime
import functools
import os
from twitchAPI.twitch import Twitch as TwitchAPI

from streamstatus.stream_host import StreamHost


class Facebook(StreamHost):

    @property
    def is_live(self):
        pass

    def get_stream_duration(self):
        pass

    def get_current_viewers(self):
        pass

    def get_credentials(self):
        # Open config.py
        config = ConfigParser()

        stream_status_path = f'{os.sep}{os.path.join(*os.path.realpath(__file__).split(os.sep)[:-2])}'
        config_file = os.path.join(stream_status_path, 'config.ini')
        config.read(config_file)
        return config['Facebook']['access_token']

    @classmethod
    def logo_name(cls):
        return 'facebook.png'


class TwitchCredentials:

    def __init__(self, client_id, secret):
        self.client_id = client_id
        self.secret = secret
