from flask import Flask, render_template

from streamstatus.companion import Companion
from streamstatus.spx_gc import SpxGc
from streamstatus.tally_arbiter import TallyArbiter

app = Flask(__name__)
pi_host = '192.168.2.51'


@app.route("/")
def index():
    comp = Companion(pi_host)
    response = f'{comp}: {comp.get_is_healthy()}'

    tally_arbiter = TallyArbiter(pi_host)
    response += f'<br>{tally_arbiter}: {tally_arbiter.get_is_healthy()}'

    spx = SpxGc(pi_host)
    response += f'<br>{spx}: {spx.get_is_healthy()}'

    apps = [comp, tally_arbiter, spx]

    return render_template("index.html", apps=apps)


if __name__ == "__main__":
    app.run(port=8001, debug=True)
