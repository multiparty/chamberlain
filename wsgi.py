import logging
import os
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from chamberlain.mockDB import DB
from chamberlain.templates import *
from chamberlain.utils import *

cardinal_DB = DB()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return "homepage"


@app.route("/")
@app.route("/index")
def index():
    """
    homepage
    """
    return "homepage"


@app.route("/api/submit", methods=["POST"])
def submit():

    if request.method == "POST":
        """
        Request format:
        {
            "workflow_name": "test-workflow",
            "party_count": 3,
            "party_list": [1,2,3],
            "data_set_id": "HRI107",
            "operation": "std-dev"
        }
        """
    # handle the POST request
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            comp_details = parse_computation_request(request_data)
        except Exception as e:
            return f'ERROR: {e}'
        # TODO return computation ID and start computation asynchronously
        return orchestrate_computation(comp_details, cardinal_DB)
    # otherwise handle the GET request
    else:
        return show_computation_form()


if __name__ != "__main__":

    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
