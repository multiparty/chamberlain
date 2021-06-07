import logging
import os
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from flask_mysqldb import MySQL
from dotenv import load_dotenv

from chamberlain.mockDB import DB
from chamberlain.templates import *
from chamberlain.utils import *

cardinal_DB = DB()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# set config for database
load_dotenv()
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
# initialize mysql client
mysql = MySQL(app)

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
            "data_set_id": "HRI107",
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
            response_msg = insert_workflow(mysql,request_data)
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
            workflows = get_workflows(mysql)
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
            workflow = get_workflow_id(mysql,id)
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
            response_msg = delete_workflow(mysql,id)
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
            response_msg = insert_dataset(mysql,request_data)
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
            datasets = get_datasets(mysql)
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
            response_msg = modify_dataset(mysql,request_data)
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
            dataset = get_dataset_id(mysql,id)
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
            response_msg = delete_dataset(mysql,id)
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
            response_msg = insert_cardinal(mysql,request_data)
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
            cardinals = get_cardinals(mysql)
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
            response_msg = modify_cardinal(mysql,request_data)
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
            cardinal = get_cardinal_id(mysql,id)
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
            response_msg = delete_cardinal(mysql,id)
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
            response_msg = insert_workflow_relationship(mysql,request_data)
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
            workflow_relationships = get_workflow_relationships(mysql)
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
            workflow_relationship = get_workflow_relationship_id(mysql,id)
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
            response_msg = delete_workflow_relationship(mysql,id)
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
    ## TODO Change the host ip back to 0.0.0.0 before committing
    app.run(host="127.0.0.1", port=port, debug=True)
