import requests
from flask import Flask, json, request
from mockDB import DB
from templates import *

cardinal_DB = DB()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/compute', methods=['GET', 'POST'])
def compute():
    '''
    Request format:
    {
      "workflow_name": "test-workflow",
      "party_count": 3,
      "party_list": [1,2,3],
      "data_set_id": "HRI107",
      "operation": "std-dev"
    }
    '''
    # handle the POST request
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            comp_details = parse_computatuon_request(request_data)
        except Exception as e:
            return f'ERROR: {e}'
        #TODO return computation ID and start computation asynchronously
        return orchestrate_computation(comp_details)
    # otherwise handle the GET request
    else:
        return show_computation_form()


def orchestrate_computation(computation_settings):
    # GET IP addresses for dataset owners
    cardinals = request_data_owners(computation_settings['data_set_id']) # should be a call to postgres or mysql
    PID1, IP1 = cardinals[0]
    payload = {
             "workflow_name": computation_settings['workflow_name'],
             "data_set_id": computation_settings['data_set_id'],
             "operation": computation_settings['operation'],
             "PID": PID1
             }
    # instruct cardinal to start jiff server
    r = requests.post('http://' + IP1 + '/api/submit', payload, timeout=1)
    if r.status_code != 200:
        error = r.get_json(force=True)
        msg = f'JIFF Server could not be started: {error}'
        raise Exception(msg)
    body = r.get_json(force=True)
    jiff_server_IP = body["JIFF_SERVER_IP"]

    responses = []
    for PID, IP in cardinals:
         payload = {
                 "workflow_name": computation_settings['workflow_name'],
                 "data_set_id": computation_settings['data_set_id'],
                 "operation": computation_settings['operation'],
                 "PID": PID,
                 "other_cardinals": [x for x in cardinals if not x == (PID, IP)],
                 "jiff_server": jiff_server_IP
                 }
         r = requests.post('http://' + IP + '/api/submit', payload, timeout=1)
         responses.append(r)
    for x in responses:
        if x.status_code != 200:
            return 'one or more jiff servers failed to start'
    return 'computation started'

def parse_computatuon_request(request_data):
    computation_settings = {}
    if request_data:
        if 'workflow_name' in request_data:
            computation_settings['workflow_name'] = request_data['workflow_name']
        else:
            raise Exception("Computation request does not contain a valid workflow_name (type: str)")

        if 'data_set_id' in request_data:
            computation_settings['data_set_id'] = request_data['data_set_id']
        else:
            raise Exception("Computation request does not contain a valid workflow_id (type: str)")

        if 'operation' in request_data:
            computation_settings['operation'] = request_data['operation']
        else:
            raise Exception("Computation request does not contain a valid operation (type: str)")
    else:
        raise Exception("Request is empty")

    return computation_settings

def request_data_owners(dataset_id):
    try:
        value = cardinal_DB.retrieve(dataset_id)
        return value
    except Exception as e:
        raise Exception("data_set_id is unknown or does not exist")
