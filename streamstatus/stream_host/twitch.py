from configparser import ConfigParser
import functools
import os
from twitchAPI.twitch import Twitch as TwitchAPI

from streamstatus.stream_host import StreamHost


class Twitch(StreamHost):

    def __init__(self, login):
        super().__init__()
        self.login = login

    @functools.cached_property
    def api(self):
        creds = self.get_credentials()
        return TwitchAPI(creds.client_id, creds.secret)

    @functools.cached_property
    def user_id(self):
        user_info = self.api.get_users(logins=[self.login])
        return user_info['data'][0]['id']

    @property
    def is_live(self):
        return True if self.get_streams()['data'] else False

    def get_streams(self):
        streams = self.api.get_streams(user_id=self.user_id)
        return streams

    def get_current_viewers(self):
        if self.is_live:
            return self.get_streams()['data'][0]['viewer_count']
        else:
            return -1

    def get_credentials(self):
        # Open config.py
        config = ConfigParser()

        stream_status_path = f'{os.sep}{os.path.join(*os.path.realpath(__file__).split(os.sep)[:-2])}'
        config_file = os.path.join(stream_status_path, 'config.ini')
        config.read(config_file)
        return TwitchCredentials(config['Twitch']['client_id'], config['Twitch']['secret'])


class TwitchCredentials:

    def __init__(self, client_id, secret):
        self.client_id = client_id
        self.secret = secret
