import asyncio
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import ast


def orchestrate_computation(computation_settings, cardinal_DB):
    # GET IP addresses for dataset owners
    cardinals = request_data_owners(computation_settings['dataset_id'], cardinal_DB)
    # add job to runningJobs table
    computation_settings['workflow_name'] = add_running_job(computation_settings, cardinal_DB, cardinals)
    # get workflow source buckets and keys
    computation_settings['workflow_source_bucket'] , computation_settings['workflow_source_key'] = cardinal_DB.get_workflow_location_from_request(computation_settings['dataset_id'],computation_settings['operation'])
    # get datasets source bucket, source key and parameters
    computation_settings['dataset_parameters'] = cardinal_DB.get_dataset_parameters_from_dataset_id(computation_settings['dataset_id'])

    PID1, IP1, ID1 = cardinals[0]
    payload = {
        "workflow_name": computation_settings['workflow_name'],
        "dataset_id": computation_settings['dataset_id'],
        "operation": computation_settings['operation'],
        "workflow_source_bucket": computation_settings['workflow_source_bucket'],
        "workflow_source_key": computation_settings['workflow_source_key'],
        "PID": PID1,
        "other_cardinals": [x for x in cardinals if not x == (PID1, IP1, ID1)],
    }
    # instruct cardinal to start jiff server
    r = requests.post(IP1 + '/api/start_jiff_server', json.dumps(payload), timeout=100)
    # print('TEXT --> ', r.text)
    if r.status_code != 200:
        error = r.json()
        msg = f'JIFF Server could not be started: {error}'
        raise Exception(msg)
    body = r.json()
    jiff_server_IP = body["JIFF_SERVER_IP"]
    # print('BODY --> ', body)

    responses = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(send_asynchronous_submits(cardinals, computation_settings, jiff_server_IP, responses))
    loop.run_until_complete(future)
    return responses


def parse_computation_request(request_data):
    computation_settings = {}
    if request_data:
        if 'dataset_id' in request_data:
            computation_settings['dataset_id'] = request_data['dataset_id']
        else:
            raise Exception("Computation request does not contain a valid dataset_id (type: str)")

        if 'operation' in request_data:
            computation_settings['operation'] = request_data['operation']
        else:
            raise Exception("Computation request does not contain a valid operation (type: str)")

        if 'party_count' in request_data:
            computation_settings['party_count'] = request_data['party_count']
        else:
            raise Exception("Computation request does not contain a valid party_count (type: int)")
    else:
        raise Exception("Request is empty")

    return computation_settings


def request_data_owners(dataset_id, cardinal_DB):
    try:
        value = cardinal_DB.retrieve(dataset_id)
        return value
    except Exception as e:
        raise Exception("dataset_id is unknown or does not exist")


def add_running_job(computation_settings, cardinal_DB, cardinals):
    running_jobs = cardinal_DB.get_running_jobs()
    workflow_name = f'workflow-{len(running_jobs)+1}'
    cardinal_ids = [c[2] for c in cardinals]
    job_payload = {
        "workflowName": workflow_name,
        "cardinals": ','.join(cardinal_ids),
        "datasetId": computation_settings['dataset_id'],
        "operation": computation_settings['operation']
    }
    try:
        cardinal_DB.insert_running_job(job_payload)
        return workflow_name
    except Exception as e:
        raise Exception(f'Error inserting new running job: {e}')


async def send_asynchronous_submits(cardinals, computation_settings, jiff_server_IP, responses):
    ip_payload = []
    for PID, IP, ID in cardinals:
        payload = {
            "workflow_name": computation_settings['workflow_name'],
            "dataset_id": computation_settings['dataset_id'],
            "operation": computation_settings['operation'],
            "cardinal_ip": IP,
            "workflow_source_bucket": computation_settings['workflow_source_bucket'],
            "workflow_source_key": computation_settings['workflow_source_key'],
            "PID": PID,
            "other_cardinals": [x for x in cardinals if not x == (PID, IP, ID)],
            "jiff_server": jiff_server_IP
        }

        try:
            parameters = computation_settings['dataset_parameters']
            parameters = ast.literal_eval(parameters.replace('false','False').replace('true','True').replace("ZP","zp"))
            payload.update(parameters)
        except:
            raise Exception("Invalid parameters field of dataset")

        ip_payload += [(IP, json.dumps(payload))]

    # adapted from:
    # https://medium.com/hackernoon/how-to-run-asynchronous-web-requests-in-parallel-with-python-3-5-without-aiohttp-264dc0f8546
    # responses = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Set any session parameters here before calling `fetch`
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                send_submit,
                *(x[0], x[1]) # Allows us to pass in multiple arguments to `fetch`
            )
            for x in ip_payload
        ]
        for response in await asyncio.gather(*tasks):
            responses += [response]

    # return responses

def send_submit(ip, payload):
    response = {"MSG": "ERR"}
    while "MSG" in response:
        response = requests.post(ip + '/api/submit', payload)
        # print(response.text)
        response = response.json()

    return response

