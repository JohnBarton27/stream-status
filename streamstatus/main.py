from flask import Flask

from streamstatus.companion import Companion
from streamstatus.tally_arbiter import TallyArbiter

app = Flask(__name__)


@app.route("/")
def index():
    comp = Companion('192.168.2.51', 8000)
    response = f'{comp}: {comp.get_is_healthy()}'

    tally_arbiter = TallyArbiter('192.168.2.51', 4455)
    response += f'<br>{tally_arbiter}: {tally_arbiter.get_is_healthy()}'

    return response


if __name__ == "__main__":
    app.run(port=8001, debug=True)
