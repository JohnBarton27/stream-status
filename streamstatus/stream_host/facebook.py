from configparser import ConfigParser
from datetime import datetime
import functools
from datetime import datetime
import json
import os
import pytz
import requests

from streamstatus.stream_host import StreamHost


class Facebook(StreamHost):

    @property
    def is_live(self):
        return self._get_current_live_video() is not None

    def _get_live_videos(self):
        url = f'https://graph.facebook.com/v12.0/{self.login}/live_videos?access_token={self.get_credentials()}'
        response = requests.get(url)
        live_videos = json.loads(response.text)['data']
        return live_videos

    def _get_current_live_video(self):
        live_videos = self._get_live_videos()
        if live_videos[0]['status'] != 'LIVE':
            return None

        video_id = live_videos[0]['id']
        url = f'https://graph.facebook.com/v12.0/{video_id}?access_token={self.get_credentials()}&fields=creation_time,live_views,status'
        response = requests.get(url)
        video_json = json.loads(response.text)

        return video_json

    def get_stream_duration(self):
        if not self.is_live:
            return -1

        video = self._get_current_live_video()
        stream_started = datetime.strptime(video['creation_time'], '%Y-%m-%dT%H:%M:%S%z')
        time_delta = pytz.timezone('America/New_York').localize(datetime.now()) - stream_started

        s = time_delta.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_timedelta = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

        return formatted_timedelta

    def get_current_viewers(self):
        if not self.is_live:
            return -1
        print(self._get_current_live_video())
        return self._get_current_live_video()['live_views']

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
