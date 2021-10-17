from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

from streamstatus.companion import Companion
from streamstatus.light_factory import LightFactory
from streamstatus.ndi_cam import NDICam
from streamstatus.spx_gc import SpxGc
from streamstatus.tally_arbiter import TallyArbiter
from streamstatus.stream_host.twitch import Twitch
from streamstatus.stream_host.youtube import YouTube

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

pi_host = '192.168.2.51'
comp = Companion(pi_host)
tally_arbiter = TallyArbiter(pi_host)
spx = SpxGc(pi_host)
gath_light_factory = LightFactory('192.168.0.104', app_name='Gathering Light Factory')
trad_light_factory = LightFactory('192.168.3.104', app_name='Traditional Light Factory')

twitch_sumc = Twitch('suntreeumc')
youtube_sumc = YouTube('UCsBehZanirQsd50CtaFhIfw', friendly_name='Suntree UMC')
youtube_mba = YouTube('UCnM5iMGiKsZg-iOlIO2ZkdQ', friendly_name='Monterey Bay Aquarium')

# Cams
ndi_cam_1 = NDICam('192.168.2.55', app_name='NDI Cam 1')
ndi_cam_2 = NDICam('192.168.2.53', app_name='NDI Cam 2')
ndi_cam_3 = NDICam('192.168.2.52', app_name='NDI Cam 3')

apps = [comp, tally_arbiter, spx, gath_light_factory, trad_light_factory]
streams = [twitch_sumc, youtube_sumc, youtube_mba]
cams = [ndi_cam_1, ndi_cam_2, ndi_cam_3]


@app.route("/")
def index():
    return render_template("index.html", apps=apps, streams=streams, cams=cams)


@socketio.on('get_statuses')
def handle_my_custom_event():
    while True:
        data = {}
        for application in apps:
            data[application.app_name] = {'status': application.get_is_healthy(), 'time': application.uptime}

        print(data)
        emit('broadcast-statuses', data, broadcast=True)
        time.sleep(2)


@socketio.on('get_viewers')
def handle_get_viewers():
    while True:
        data = {}
        for stream in streams:
            data[str(stream)] = {
                'duration': stream.get_stream_duration(),
                'viewers': stream.get_current_viewers()
            }

        print(data)
        emit('broadcast-viewers', data, broadcast=True)
        time.sleep(30)


@socketio.on('get_cams')
def handle_get_cams():
    while True:
        data = {}
        for cam in cams:
            data[cam.app_name] = {'status': cam.get_is_healthy(), 'time': cam.uptime}

        print(data)
        emit('broadcast-cams', data, broadcast=True)
        time.sleep(2)


if __name__ == "__main__":
    app.run(port=8001, debug=True)
