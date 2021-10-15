from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

from streamstatus.companion import Companion
from streamstatus.light_factory import LightFactory
from streamstatus.spx_gc import SpxGc
from streamstatus.tally_arbiter import TallyArbiter
from streamstatus.stream_host.twitch import Twitch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

pi_host = '192.168.2.51'
comp = Companion(pi_host)
tally_arbiter = TallyArbiter(pi_host)
spx = SpxGc(pi_host)
gath_light_factory = LightFactory('192.168.0.104', app_name='Gathering Light Factory')
trad_light_factory = LightFactory('192.168.3.104', app_name='Traditional Light Factory')

twitch_gabz = Twitch('ChaoticGabz')
twitch_sumc = Twitch('suntreeumc')

# apps = [comp, tally_arbiter, spx, gath_light_factory, trad_light_factory]
apps = [comp]
streams = [twitch_gabz, twitch_sumc]


@app.route("/")
def index():
    return render_template("index.html", apps=apps, streams=streams)


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
        time.sleep(2)


if __name__ == "__main__":
    app.run(port=8001, debug=True)
