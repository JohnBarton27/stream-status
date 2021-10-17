from streamstatus.stream_host import StreamHost

from configparser import ConfigParser
from datetime import datetime
import functools
import json
import os
import requests


class YouTube(StreamHost):

    @property
    def is_live(self):
        return len(self.channel_live_broadcasts) > 0

    @property
    def channel_live_broadcasts(self):
        url = f'https://youtube.googleapis.com/youtube/v3/search?eventType=live&type=video&channelId={self.login}&maxResults=50&key={self.get_credentials()}'
        response = requests.get(url)
        return json.loads(response.text)['items']

    def get_single_live_video(self):
        video = self.channel_live_broadcasts[0]
        video_id = video['id']['videoId']
        url = f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics%2CliveStreamingDetails&id={video_id}&maxResults=50&key={self.get_credentials()}'
        response = requests.get(url)
        return json.loads(response.text)['items'][0]

    def get_stream_duration(self):
        if not self.is_live:
            return -1

        stream_started = datetime.strptime(self.get_single_live_video()['liveStreamingDetails']['actualStartTime'], '%Y-%m-%dT%H:%M:%SZ')
        time_delta = datetime.utcnow() - stream_started

        s = time_delta.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_timedelta = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

        return formatted_timedelta

    def get_current_viewers(self):
        if not self.is_live:
            return -1

        return self.get_single_live_video()['liveStreamingDetails']['concurrentViewers']

    def get_credentials(self):
        # Open config.py
        config = ConfigParser()

        stream_status_path = f'{os.sep}{os.path.join(*os.path.realpath(__file__).split(os.sep)[:-2])}'
        config_file = os.path.join(stream_status_path, 'config.ini')
        config.read(config_file)
        return config['YouTube']['api_key']

    @classmethod
    def logo_name(cls):
        return 'youtube.png'
