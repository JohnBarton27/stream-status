import requests

from streamstatus.stream_host.facebook import Facebook
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import json

facebook = Facebook('SuntreeUMC')
url = f'https://graph.facebook.com/v12.0/{facebook.login}/live_videos?access_token={facebook.get_credentials()}'
response = requests.get(url)
live_videos = json.loads(response.text)['data']
video_id = live_videos[1]['id']

url = f'https://graph.facebook.com/v12.0/{video_id}?access_token={facebook.get_credentials()}&fields=creation_time,live_views,status'
response = requests.get(url)
video_json = json.loads(response.text)
print(json.dumps(video_json, indent=4, sort_keys=True))

