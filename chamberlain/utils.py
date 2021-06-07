import asyncio
import json
import requests
from concurrent.futures import ThreadPoolExecutor


def orchestrate_computation(computation_settings, cardinal_DB):
    # GET IP addresses for dataset owners
    # TODO: make this a call to postgres or mysql
    cardinals = request_data_owners(computation_settings['dataset_id'], cardinal_DB)
    PID1, IP1 = cardinals[0]
    payload = {
        "workflow_name": computation_settings['workflow_name'],
        "dataset_id": computation_settings['dataset_id'],
        "operation": computation_settings['operation'],
        "PID": PID1,
        "other_cardinals": [x for x in cardinals if not x == (PID1, IP1)],
    }
    # instruct cardinal to start jiff server
    r = requests.post(IP1 + '/api/start_jiff_server', json.dumps(payload), timeout=1)
    # print('TEXT --> ', r.text)
    if r.status_code != 200:
        error = r.json()
        msg = f'JIFF Server could not be started: {error}'
        raise Exception(msg)
    body = r.json()
    jiff_server_IP = body["JIFF_SERVER_IP"]+":8080"
    # print('BODY --> ', body)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(send_asynchronous_submits(cardinals, computation_settings, jiff_server_IP))
    loop.run_until_complete(future)


def parse_computation_request(request_data):
    computation_settings = {}
    if request_data:
        if 'workflow_name' in request_data:
            computation_settings['workflow_name'] = request_data['workflow_name']
        else:
            raise Exception("Computation request does not contain a valid workflow_name (type: str)")

        if 'dataset_id' in request_data:
            computation_settings['dataset_id'] = request_data['dataset_id']
        else:
            raise Exception("Computation request does not contain a valid dataset_id (type: str)")

        if 'operation' in request_data:
            computation_settings['operation'] = request_data['operation']
        else:
            raise Exception("Computation request does not contain a valid operation (type: str)")
    else:
        raise Exception("Request is empty")

    return computation_settings


def request_data_owners(dataset_id, cardinal_DB):
    try:
        value = cardinal_DB.retrieve(dataset_id)
        return value
    except Exception as e:
        raise Exception("dataset_id is unknown or does not exist")


async def send_asynchronous_submits(cardinals, computation_settings, jiff_server_IP):
    ip_payload = []
    for PID, IP in cardinals:
        payload = {
            "workflow_name": computation_settings['workflow_name'],
            "dataset_id": computation_settings['dataset_id'],
            "operation": computation_settings['operation'],
            "PID": PID,
            "other_cardinals": [x for x in cardinals if not x == (PID, IP)],
            "jiff_server": jiff_server_IP
        }
        ip_payload += [(IP, json.dumps(payload))]

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
            pass


def send_submit(ip, payload):
    response = {"MSG": "ERR"}
    while "MSG" in response:
        response = requests.post(ip + '/api/submit', payload)
        # print(response.text)
        response = response.json()

    return response

# chamberlain db crud operation helper functions

## workflow
def insert_workflow(mysql, payload):
    '''
        This function inserts workflow in the MySQL chamberlain database
        params:
            mysql: Database connection object
            req: request payload  - dict
    '''

    if 'operationName' in payload and 'workflowId' in payload:
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO chamberlain.workflows (workflowId,operationName) VALUES (%s,%s)'
        cursor.execute(query,( payload['workflowId'],payload['operationName'] ))
        mysql.connection.commit()
        cursor.close()

        return 'successfull'
    else:
        return "request format not correct"

def get_workflows(mysql):
    '''
        This function returns workflow in the MySQL chamberlain database
        params:
            mysql: Database connection object
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.workflows'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def get_workflow_id(mysql,id):
    '''
        This function returns workflow with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of workflow - string
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.workflows WHERE workflowId="' + str(id) + '"'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def delete_workflow(mysql,id):
    '''
        This function deletes workflow with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of workflow - string
    '''

    cursor = mysql.connection.cursor()
    query = 'DELETE FROM chamberlain.workflows WHERE workflowId="' + str(id) + '"'
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()

    return 'successful'

## dataset
def insert_dataset(mysql, payload):
    '''
        This function inserts dataset in the MySQL chamberlain database
        params:
            mysql: Database connection object
            req: request payload  - dict
    '''

    if 'datasetSchema' in payload and 'datasetId' in payload:
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO chamberlain.datasets (datasetId,datasetSchema) VALUES (%s,%s)'
        cursor.execute(query,( payload['datasetId'],payload['datasetSchema'] ))
        mysql.connection.commit()
        cursor.close()

        return 'successfull'
    else:
        return "request format not correct"
    
def get_datasets(mysql):
    '''
        This function returns dataset in the MySQL chamberlain database
        params:
            mysql: Database connection object
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.datasets'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def get_dataset_id(mysql,id):
    '''
        This function returns dataset with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of dataset - string
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.datasets WHERE datasetId="' + str(id) + '"'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def delete_dataset(mysql,id):
    '''
        This function deletes dataset with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of dataset - string
    '''

    cursor = mysql.connection.cursor()
    query = 'DELETE FROM chamberlain.datasets WHERE datasetId="' + str(id) + '"'
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()

    return 'successful'

def modify_dataset(mysql, payload):

    '''
        This function modifies dataset in the MySQL chamberlain database
        params:
            mysql: Database connection object
            req: request payload  - dict
    '''

    if 'datasetSchema' in payload and 'datasetId' in payload:
        cursor = mysql.connection.cursor()
        query = 'UPDATE chamberlain.datasets SET datasetSchema =%s WHERE datasetId=%s'
        cursor.execute(query,( payload['datasetSchema'],payload['datasetId'] ))
        mysql.connection.commit()
        cursor.close()

        return 'successfull'
    
    else:
        return "request format not correct"

## cardinal
def insert_cardinal(mysql, payload):
    '''
        This function inserts cardinal in the MySQL chamberlain database
        params:
            mysql: Database connection object
            req: request payload  - dict
    '''

    if 'cardinalIp' in payload and 'cardinalId' in payload:
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO chamberlain.cardinals (cardinalId,cardinalIp) VALUES (%s,%s)'
        cursor.execute(query,( payload['cardinalId'],payload['cardinalIp'] ))
        mysql.connection.commit()
        cursor.close()

        return 'successfull'
    else:
        return "request format not correct"
    
def get_cardinals(mysql):
    '''
        This function returns cardinal in the MySQL chamberlain database
        params:
            mysql: Database connection object
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.cardinals'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def get_cardinal_id(mysql,id):
    '''
        This function returns cardinal with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of cardinal - string
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.cardinals WHERE cardinalId="' + str(id) + '"'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def delete_cardinal(mysql,id):
    '''
        This function deletes cardinal with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of cardinal - string
    '''

    cursor = mysql.connection.cursor()
    query = 'DELETE FROM chamberlain.cardinals WHERE cardinalId="' + str(id) + '"'
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()

    return 'successful'

def modify_cardinal(mysql, payload):
    '''
        This function modifies cardinal in the MySQL chamberlain database
        params:
            mysql: Database connection object
            req: request payload  - dict
    '''

    if 'cardinalIp' in payload and 'cardinalId' in payload:
        cursor = mysql.connection.cursor()
        query = 'UPDATE chamberlain.cardinals SET cardinalIp =%s WHERE cardinalId=%s'
        cursor.execute(query,( payload['cardinalIp'],payload['cardinalId'] ))
        mysql.connection.commit()
        cursor.close()

        return 'successfull'
    
    else:
        return "request format not correct"

## workflow relationship
def insert_workflow_relationship(mysql, payload):
    '''
        This function inserts workflow relationship in the MySQL chamberlain database
        params:
            mysql: Database connection object
            req: request payload  - dict
    '''

    if 'workflowRelationshipId' in payload and 'datasetId' in payload and 'workflowId' in payload:
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO chamberlain.workflowrelationships (workflowRelationshipId,datasetId,workflowId) VALUES (%s,%s,%s)'
        cursor.execute(query,( payload['workflowRelationshipId'],payload['datasetId'],payload['workflowId'] ))
        mysql.connection.commit()
        cursor.close()

        return 'successfull'
    else:
        return "request format not correct"
    
def get_workflow_relationships(mysql):
    '''
        This function returns workflow_relationship in the MySQL chamberlain database
        params:
            mysql: Database connection object
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.workflowrelationships'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def get_workflow_relationship_id(mysql,id):
    '''
        This function returns workflow_relationship with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of cardinal - string
    '''

    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM chamberlain.workflowrelationships WHERE workflowRelationshipId="' + str(id) + '"'
    cursor.execute(query)
    data = list(cursor.fetchall())
    cursor.close()

    return data

def delete_workflow_relationship(mysql,id):
    '''
        This function deletes workflow_relationship with specified in from the MySQL chamberlain database
        params:
            mysql: Database connection object
            id: id of cardinal - string
    '''

    cursor = mysql.connection.cursor()
    query = 'DELETE FROM chamberlain.workflowrelationships WHERE workflowRelationshipId="' + str(id) + '"'
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()

    return 'successful'
