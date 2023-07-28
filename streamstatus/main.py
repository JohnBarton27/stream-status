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
from streamstatus.checklist_item import ChecklistItem
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
from streamstatus.dao.wv_dao import WelcomeVideoDao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# INITIALIZE DAOS
app_dao = ApplicationDao()
wv_dao = WelcomeVideoDao()

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
# welcome_video = WelcomeVideo.get_from_file('/home/streaming/Videos/Welcome to Worship January.mp4')

streams = [twitch_sumc] #, facebook_sumc]
cams = [ndi_cam_1, ndi_cam_2, ndi_cam_3, drum_cam, piano_cam, ptz_1, ptz_2]
events = None

# FROM DATABASE
apps_from_db = None
welcome_video = None
hardware = ["WebPresenter_Bitrate", "WebPresenter_Cache", "WebPresenter_State"]
webpresenter_bitrate = 0
webpresenter_cache = 0
webpresenter_state = 0

# CHECKLIST ITEMS
checklist_items = []
checklist_items.append(ChecklistItem('Start OBS'))
checklist_items.append(ChecklistItem('Start Companion'))
checklist_items.append(ChecklistItem('Review both Worship Orders'))
checklist_items.append(ChecklistItem('Download Videos from OneDrive'))
checklist_items.append(ChecklistItem('Load Videos into OBS'))
checklist_items.append(ChecklistItem('Setup SPX Titles'))
checklist_items.append(ChecklistItem('[GATH] Update titles/descriptions in Restream'))
checklist_items.append(ChecklistItem('[GATH] Confirm PTZ Presets'))
checklist_items.append(ChecklistItem('[GATH] Setup Podium Camera'))
checklist_items.append(ChecklistItem('[GATH] Setup Cameras on Stage'))
checklist_items.append(ChecklistItem('[GATH] Setup Tally Lights'))
checklist_items.append(ChecklistItem('[TRAD] Update titles/descriptions in Restream'))
checklist_items.append(ChecklistItem('[TRAD] Confirm PTZ Presets'))


def update_from_db():
    global apps_from_db, welcome_video, events
    apps_from_db = app_dao.get_all()
    welcome_video = wv_dao.get_all()[-1] if wv_dao.get_all() else None
    gathering.welcome = welcome_video
    traditional.welcome = welcome_video
    events = gathering.get_all_events() + traditional.get_all_events()


# DISPLAYS
@app.route("/")
def index():
    return render_template("index.html", apps=apps_from_db, hardware=hardware, streams=streams, cams=cams, events=events)


@app.route("/config")
def config():
    return render_template("config.html", apps=apps_from_db)


@app.route("/checklist")
def checklist():
    return render_template("checklist.html", checklist_items=checklist_items)


# REST API
@app.route('/application', methods=['PUT'])
def create_application():
    app_hostname = request.form['hostname']
    app_port = int(request.form['port'])
    app_name = request.form['name']

    app = Application(app_hostname, app_port, app_name=app_name)
    app_dao.create(app)

    update_from_db()
    return 'Success!'


@app.route('/welcome_video', methods=['PUT'])
def update_welcome_video():
    wv_filepath = request.form['filepath']
    wv = WelcomeVideo.get_from_file(wv_filepath)
    wv_dao.create(wv)

    update_from_db()

    gathering.welcome = welcome_video
    traditional.welcome = welcome_video
    return 'Success!'


@app.route('/api/configured_apps', methods=['GET'])
def configured_applications():
    update_from_db()

    return render_template("elements/app_config.html", apps=apps_from_db)


@app.route('/api/configured_welcome_video', methods=['GET'])
def configured_welcome_video():
    update_from_db()

    return render_template("elements/welcome_video_config.html", welcome_video=welcome_video)


@app.route('/api/webpresenter/bitrate/<bitrate>')
def set_webpresenter_bitrate(bitrate):
    global webpresenter_bitrate
    webpresenter_bitrate = f'{round(int(bitrate) / 1000)} kpbs'
    return 'SUCCESS'


@app.route('/api/webpresenter/cache/<cache>')
def set_webpresenter_cache(cache):
    global webpresenter_cache
    webpresenter_cache = f'{cache}'
    return 'SUCCESS'


@app.route('/api/webpresenter/state/<state>')
def set_webpresenter_state(state):
    global webpresenter_state
    webpresenter_state = f'{state}'
    return 'SUCCESS'


@app.route('/api/update_checkbox_status', methods=['POST'])
def update_checkbox_status():
    data = request.get_json()
    checkbox_id = data.get('id')
    checked = data.get('checked')

    for checkbox in checklist_items:
        if checkbox.name == checkbox_id:
            checkbox.checked = checked
            return f'Setting {checkbox.name} to {checkbox.checked}'

    return "FAILED TO UPDATE"


# SOCKETS
@socketio.on('get_hardware')
def handle_hardware():
    while True:
        data = {'bitrate': webpresenter_bitrate, 'cache': webpresenter_cache, 'state': webpresenter_state}
        emit('broadcast-hardware', data, broadcast=True)
        time.sleep(5)


@socketio.on('get_statuses')
def handle_my_custom_event():
    while True:
        data = {}
        for application in apps_from_db:
            data[application.app_name] = {'status': application.get_is_healthy(), 'time': application.uptime}

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

        emit('broadcast-viewers', data, broadcast=True)
        time.sleep(30)


@socketio.on('get_cams')
def handle_get_cams():
    while True:
        data = {}
        for cam in cams:
            data[cam.app_name] = {'status': cam.get_is_healthy(), 'time': cam.uptime}

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
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        hostname TEXT NOT NULL,
                        port INTEGER NOT NULL,
                        name TEXT NOT NULL
                    );                
                """)

            # VIDEO
            conn.execute("""
                    CREATE TABLE welcome_video (
                        filepath TEXT NOT NULL,
                        length INT NOT NULL 
                    )
            """)


if __name__ == "__main__":
    connect_to_database()
    update_from_db()

    app.run(host="0.0.0.0", port=8001, debug=True)
