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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the GET request
    else:
        return show_computation_form()


# Chamberlain dataset CRUD endpoints

## Workflow endpoints
@app.route("/api/workflow", methods=["POST","GET"])
def handle_workflow_req():

    # handle the POST request
    if request.method == 'POST':
        """
        Request format:
        {
            "worklowId":"WK103",
            "operationName": "SUM"
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            workflows = cardinal_DB.get_workflows(mysql_db)
            response = {
                "workflows":workflows
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

@app.route("/api/workflow/<id>", methods=["GET","DELETE"])
def handle_workflow_id_req(id):

    # handle the GET request
    if request.method == 'GET':
        try:
            workflow = cardinal_DB.get_workflow_id(id)
            response = {
                "workflow": workflow
            }
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_workflow(id)
            response = {
                "MSG":response_msg
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

## Dataset endpoints
@app.route("/api/dataset", methods=["POST","GET","PUT"])
def handle_dataset_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "datasetId":"HRI101",
                "datasetSchema": "age,location,height"
                "cardinalId":[list of cardinal ids]
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            datasets = cardinal_DB.get_datasets()
            response = {
                "datasets":datasets
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
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
                "datasetSchema": "age,location,height"
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

@app.route("/api/dataset/<id>", methods=["GET","DELETE"])
def handle_dataset_id_req(id):

    # handle the GET request
    if request.method == 'GET':
        try:
            dataset = cardinal_DB.get_dataset_id(id)
            response = {
                "dataset": dataset
            }
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_dataset(id)
            response = {
                "MSG":response_msg
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

## Cardinal endpoints
@app.route("/api/cardinal", methods=["POST","GET","PUT"])
def handle_cardinal_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "cardinalId":"cardinal023",
                "cardinalIp": "12.23.34.45"
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            cardinals = cardinal_DB.get_cardinals()
            response = {
                "cardinals":cardinals
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

@app.route("/api/cardinal/<id>", methods=["GET","DELETE"])
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_cardinal(id)
            response = {
                "MSG":response_msg
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

## Workflow Relationship endpoints
@app.route("/api/workflow-relationship", methods=["POST","GET"])
def handle_workflow_relationship_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "workflowRelationshipId":"WR109",
                "datasetId": "HRI007",
                "workflowId":"WK103"
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            workflow_relationships = cardinal_DB.get_workflow_relationships()
            response = {
                "workflow_relationships":workflow_relationships
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/workflow-relationship/<id>", methods=["GET","DELETE"])
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_workflow_relationship(id)
            response = {
                "MSG":response_msg
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


## Storage Relationship endpoints
@app.route("/api/storage-relationship", methods=["POST","GET"])
def handle_storage_relationship_req():

    # handle the POST request
    if request.method == 'POST':
        """
            Request format:
            {
                "storageRelationshipId":"ST104",
                "datasetId": "HRI007",
                "cardinalId1":"cardinal023",
                "cardinalId2":"caridnal541",
                "cardinalId3":"cardinal346"
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)

    # otherwise handle the GET request
    elif request.method == "GET":
        try:
            storage_relationships = cardinal_DB.get_storage_relationships()
            response = {
                "storage_relationships":storage_relationships
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)


@app.route("/api/storage-relationship/<id>", methods=["GET","DELETE"])
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
                "ERR": e
            }
            app.logger.error(f"Error sending request: {e}")
            return jsonify(response)

        return jsonify(response)
    # otherwise handle the DELETE request
    elif request.method == "DELETE":
        try:
            response_msg = cardinal_DB.delete_storage_relationship(id)
            response = {
                "MSG":response_msg
            } 
            
        except Exception as e:
            print(e)
            response = {
                "ERR": e
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
    app.run(host="0.0.0.0", port=port, debug=True)
