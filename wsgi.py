import logging
import os
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from chamberlain.DB import DB
from chamberlain.templates import *
from chamberlain.utils import *

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# initialize database class
cardinal_DB = DB()


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

    # handle the POST request
    if request.method == 'POST':
        """
        Request format:
        {
            "workflow_name": "test-workflow",
            "party_count": 3,
            "party_list": [1,2,3],
            "dataset_id": "HRI107",
            "operation": "std-dev"
        }
        """
        try:
            request_data = request.get_json()
            comp_details = parse_computation_request(request_data)
            # TODO return computation ID and start computation asynchronously
            msg = orchestrate_computation(comp_details, cardinal_DB)
            response = {"MSG": msg}
        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the GET request
    else:
        return show_computation_form()


# ################# #
# DB CRUD ENDPOINTS #
# ################# #

# -------------- #
# WORKFLOW TABLE #
# -------------- #
@app.route("/api/workflow", methods=["POST", "GET", "PUT"])
def handle_workflow_req():

    # handle the POST request
    if request.method == 'POST':
        """
        Request format:
        {
            "worklowId":"WK103",
            "operationName": "SUM",
            "datasetId": "HRI0",
            "sourceBucket": "bucket-name",
            "sourceKey":"some/path/",
            "description":"description of workflow"

        }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.insert_workflow(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # handle the GET request
    elif request.method == "GET":
        try:
            workflows = cardinal_DB.get_workflows()
            response = {
                "workflows": workflows
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle PUT request method
    elif request.method == 'PUT':
        """
            Request format:
            {
                "worklowId":"WK103",
                "key": "value" 
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.modify_workflow(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/workflow/<workflowId>", methods=["GET", "DELETE"])
def handle_workflow_id_req(workflowId):

    # handle the GET request
    if request.method == 'GET':
        try:
            workflow = cardinal_DB.get_workflow_id(workflowId)
            response = {
                "workflow": workflow
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_workflow(workflowId)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


# ------------- #
# DATASET TABLE #
# ------------- #
@app.route("/api/dataset", methods=["POST", "GET", "PUT"])
def handle_dataset_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "datasetId":"HRI101",
                "datasetSchema": "age,location,height",
                "backend":"backend-name",
                "parameters":"{ "bigNumber": False, "negativeNumber":False, "fixedPoint":False, "integerDigits":0, 
                    "decimalDigits": 0, "ZP": 16777729}", # stringified dict of parameters
                "description":"some description"
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.insert_dataset(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            datasets = cardinal_DB.get_datasets()
            response = {
                "datasets": datasets
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle PUT request method
    elif request.method == 'PUT':
        """
            Request format:
            {
                "datasetId":"HRI101",
                "key": "value" 
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.modify_dataset(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/dataset/<datasetId>", methods=["GET", "DELETE"])
def handle_dataset_id_req(datasetId):

    # handle the GET request
    if request.method == 'GET':
        try:
            dataset = cardinal_DB.get_dataset_id(datasetId)
            response = {
                "dataset": dataset
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_dataset(datasetId)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

# -------------- #
# CARDINAL TABLE #
# -------------- #
@app.route("/api/cardinal", methods=["POST", "GET", "PUT"])
def handle_cardinal_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "cardinalId":"cardinal023",
                "cardinalIp": "12.23.34.45",
                "description": "some description"
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.insert_cardinal(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            cardinals = cardinal_DB.get_cardinals()
            response = {
                "cardinals": cardinals
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle PUT request method
    elif request.method == 'PUT':
        """
            Request format:
            {
                "cardinalId":"cardinal023",
                "cardinalIp": "12.23.34.45"
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.modify_cardinal(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/cardinal/<id>", methods=["GET", "DELETE"])
def handle_cardinal_id_req(id):

    # handle the GET request
    if request.method == 'GET':
        try:
            cardinal = cardinal_DB.get_cardinal_id(id)
            response = {
                "cardinal": cardinal
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_cardinal(id)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


# ---------------------------- #
# WORKFLOW_RELATIONSHIPS TABLE #
# ---------------------------- #
@app.route("/api/workflow-relationship", methods=["POST", "GET", "PUT"])
def handle_workflow_relationship_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "workflowRelationshipId":"WR109",
                "datasetId": "HRI007",
                "workflowId":"WK103",
                "description":"some description"
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.insert_workflow_relationship(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle the GET request
    elif request.method == "GET":
        try:
            workflow_relationships = cardinal_DB.get_workflow_relationships()
            response = {
                "workflow_relationships": workflow_relationships
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle the PUT request
    elif request.method == "PUT":
        """
            Request format:
            {
                "workflowRelationshipId":"WR109",
                key: value
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.modify_workflow_relationship(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/workflow-relationship/<id>", methods=["GET", "DELETE"])
def handle_workflow_relationship_id_req(id):

    # handle the GET request
    if request.method == 'GET':
        try:
            workflow_relationship = cardinal_DB.get_workflow_relationship_id(id)
            response = {
                "workflow_relationship": workflow_relationship
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_workflow_relationship(id)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


# --------------------------- #
# STORAGE_RELATIONSHIPS TABLE #
# --------------------------- #
@app.route("/api/storage-relationship", methods=["POST", "GET", "PUT"])
def handle_storage_relationship_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "datasetId": "HRI007",
                "cardinals":"cardinal023,cardinal346,cardinal541",
                "description":"some description""
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.insert_storage_relationship(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle the GET request
    elif request.method == "GET":
        try:
            storage_relationships = cardinal_DB.get_storage_relationships()
            response = {
                "storage_relationships": storage_relationships
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle the PUT request
    elif request.method == "PUT":
        """
            Request format:
            {
                "storageRelationshipId":123,
                "key": "value" 
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.modify_storage_relationship(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/storage-relationship/<id>", methods=["GET", "DELETE"])
def handle_storage_relationship_id_req(id):

    # handle the GET request
    if request.method == 'GET':
        try:
            storage_relationship = cardinal_DB.get_storage_relationship_id(id)
            response = {
                "storage_relationship": storage_relationship
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_storage_relationship(id)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


# ------------------ #
# RUNNING JOBS TABLE #
# ------------------ #

@app.route("/api/running-jobs", methods=["GET", "PUT"])
def handle_running_jobs_req():
    if request.method == "GET":
        try:
            running_jobs = cardinal_DB.get_running_jobs()
            response = {
                "running_jobs": running_jobs
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # handle the PUT request
    elif request.method == "PUT":
        """
            Request format:
            {
                "workflow_name":<string>",
                "cpu_usage": <float> (optional),
                "memory_usage": <float> (optional)
            }
        """
        try:
            request_data = request.get_json()
            response_msg = cardinal_DB.add_stats_to_running_job(request_data)
            response = {
                "MSG": response_msg
            }

        except Exception as e:
            print(e)
            response = {
                "ERR": str(e)
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


if __name__ != "__main__":

    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="127.0.0.1", port=port, debug=True)
