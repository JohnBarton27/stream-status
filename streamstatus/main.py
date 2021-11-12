# STANDARD/THIRDPARTY IMPORTS
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import logging
import sqlite3 as sl
import time
from urllib.request import pathname2url

# STREAMSTATUS IMPORTS
from streamstatus.application import Application
from streamstatus.companion import Companion
from streamstatus.light_factory import LightFactory
from streamstatus.ndi_cam import NDICam
from streamstatus.ptz_cam import PTZCam
from streamstatus.spx_gc import SpxGc
from streamstatus.tally_arbiter import TallyArbiter
from streamstatus.stream_host.facebook import Facebook
from streamstatus.stream_host.twitch import Twitch
from streamstatus.stream_host.youtube import YouTube
from streamstatus.event import Event, SundayEvent, Service
from streamstatus.video import WelcomeVideo

# DAO IMPORTS
from streamstatus.dao.application_dao import ApplicationDao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# INITIALIZE DAOS
app_dao = ApplicationDao()

pi_host = '192.168.2.51'
comp = Companion(pi_host)
tally_arbiter = TallyArbiter(pi_host)
spx = SpxGc(pi_host)
gath_light_factory = LightFactory('192.168.0.104', app_name='Gathering Light Factory')
trad_light_factory = LightFactory('192.168.3.104', app_name='Traditional Light Factory')

twitch_sumc = Twitch('suntreeumc')
# youtube_sumc = YouTube('UCsBehZanirQsd50CtaFhIfw', friendly_name='Suntree UMC')
# youtube_mba = YouTube('UCnM5iMGiKsZg-iOlIO2ZkdQ', friendly_name='Monterey Bay Aquarium')
facebook_sumc = Facebook('SuntreeUMC')

# Cams
ndi_cam_1 = NDICam('192.168.2.55', app_name='NDI Cam 1')
ndi_cam_2 = NDICam('192.168.2.53', app_name='NDI Cam 2')
ndi_cam_3 = NDICam('192.168.2.52', app_name='NDI Cam 3')
drum_cam = NDICam('192.168.2.54', app_name='Drum Cam')
piano_cam = NDICam('192.168.2.69', app_name='Piano Cam')
ptz_1 = PTZCam('192.168.2.201', app_name='PTZ 1')
ptz_2 = PTZCam('192.168.2.200', app_name='PTZ 2')


# Events
gathering = Service('Gath', hour=9, minute=30)
traditional = Service('Trad', hour=11, minute=0)

# videos
welcome_video = WelcomeVideo.get_from_file('/home/streaming/Videos/11-7-21/Mike Welcome 11-7.mp4')
gathering.welcome = welcome_video
traditional.welcome = welcome_video

apps = [comp, tally_arbiter, spx, gath_light_factory, trad_light_factory]
streams = [twitch_sumc] #, facebook_sumc]
cams = [ndi_cam_1, ndi_cam_2, ndi_cam_3, drum_cam, piano_cam, ptz_1, ptz_2]
events = gathering.get_all_events() + traditional.get_all_events()


# DISPLAYS
@app.route("/")
def index():
    return render_template("index.html", apps=apps, streams=streams, cams=cams, events=events)


# REST API
@app.route('/application', methods=['PUT'])
def create_application():
    app_hostname = request.form['hostname']
    app_port = int(request.form['port'])
    app_name = request.form['name']

    app = Application(app_hostname, app_port, app_name=app_name)
    app_dao.create(app)


# SOCKETS
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


@socketio.on('get_events')
def handle_get_events():
    while True:
        data = {}
        for event in events:
            data[event.name] = {'time_remaining': event.get_time_remaining(),
                                'danger_zone': event.in_danger_zone,
                                'extreme_danger_zone': event.in_extreme_danger_zone,
                                'id': event.id}

        print(data)
        emit('broadcast-events', data, broadcast=True)
        time.sleep(1)


def connect_to_database():
    db_name = 'stream_status.db'
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(db_name))
        sl.connect(dburi, uri=True)
        logging.info('Found existing database.')
    except sl.OperationalError:
        # handle missing database case
        logging.warning('Could not find database - will initialize an empty one!')
        conn = sl.connect(db_name)

        # Setup Tables
        with conn:
            # APPLICATION
            conn.execute("""
                    CREATE TABLE application (
                        id TEXT NOT NULL PRIMARY KEY,
                        hostname TEXT NOT NULL,
                        port INTEGER NOT NULL,
                        name TEXT NOT NULL
                    );                
                """)


if __name__ == "__main__":
    connect_to_database()

    app.run(port=8001, debug=True)
