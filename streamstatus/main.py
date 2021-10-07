from flask import Flask

from streamstatus.companion import Companion

app = Flask(__name__)


@app.route("/")
def index():
    comp = Companion('192.168.2.51', 8000)
    response = f'{comp}: {comp.get_is_healthy()}'
    return response


if __name__ == "__main__":
    app.run(port=8001, debug=True)
