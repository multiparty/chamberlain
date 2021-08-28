import os
import json
import time
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv


class DB:
    """
    Simple DB interface for the server to interact with
    a delay can be introduced to simulate computation time
    """
    def __init__(self):
        # load config for database
        load_dotenv()
        try:

            # initialize mysql client
            self.conn = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST'),
                port=int(os.environ.get('MYSQL_PORT')),
                user=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD'),
                database=os.environ.get('MYSQL_DB'),
            )
            self.database_name = os.environ.get('MYSQL_DB')
        except Exception as e:
            print(e)

    def retrieve(self, key: str, delay: float = 0.0):
        if delay > 0.0:
            time.sleep(delay)

        storage_relationship = self.get_storage_relationship_from_dataset_id(key)
        cardinalIds = storage_relationship[0][2].split(',')
        cardinalIps = self.get_cardinal_ips_from_ids(cardinalIds)
        owners = ['http://' + ip if 'http://' not in ip else ip for ip in cardinalIps]
        owners = [(i+1, ip, cardinalIds[i]) for i, ip in enumerate(owners)]

        return owners

    def get_running_jobs(self):
        query = 'SELECT * from ' + self.database_name + '.runningJobs'
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = list(cursor.fetchall())
        cursor.close()

        return result

    def insert_running_job(self, payload):
        """
            This function will add a new running job on submission of a computation to chamberlain
            params:
                datasetId: which dataset to run the computation over
                operation: which operation to run
        """

        cols = ['workflowName','cardinals', 'datasetId', 'operation']
        identifier_str = '(' + ','.join(['%s' for i in range(len(cols))]) + ')'
        columns_str = '(' + ','.join(cols) + ')'

        flag = all([True for col in cols if col in payload])

        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO ' + self.database_name + '.runningJobs ' + columns_str + ' VALUES ' + identifier_str
            values_tuple = tuple([payload[col] for col in cols])
            cursor.execute(query, values_tuple)
            self.conn.commit()
            cursor.close()

            return 'successful'
        else:
            raise Exception("request format not correct")

    def add_stats_to_running_job(self, payload):
        if 'workflow_name' in payload:
            stats_attributes = ['cardinals', 'cpuUsage', 'memoryUsage', 'submittedStats']

            select_query = 'SELECT ' + ','.join(stats_attributes) + ' FROM ' + self.database_name +\
                '.runningJobs WHERE workflowName = "' + payload['workflow_name'] + '"'
            cursor = self.conn.cursor()
            cursor.execute(select_query)
            select_result = list(cursor.fetchall())[0]
            num_cardinals = len(select_result[0].split(','))
            num_submitted = select_result[3]
            if num_submitted >= num_cardinals:
                raise Exception("Already reached max number of stats submissions for this workflow")

            if 'cpu_usage' not in payload and 'memory_usage' not in payload:
                raise Exception("No fields given to update")

            update_clause = 'UPDATE ' + self.database_name + '.runningJobs SET '
            where_clause = ' WHERE workflowName = "' + payload['workflow_name'] + '"'
            if 'cpu_usage' in payload:
                if num_submitted == 0:
                    set_query = update_clause + 'cpuUsage = ' + str(payload['cpu_usage']) + where_clause
                    cursor.execute(set_query)
                    self.conn.commit()
                else:
                    prior = select_result[1] * num_submitted
                    new_avg = (prior + payload['cpu_usage'])/(num_submitted+1)
                    set_query = update_clause + 'cpuUsage = ' + str(new_avg) + where_clause
                    cursor.execute(set_query)
                    self.conn.commit()

            if 'memory_usage' in payload:
                if num_submitted == 0:
                    set_query = update_clause + 'memoryUsage = ' + str(payload['memory_usage']) + where_clause
                    cursor.execute(set_query)
                    self.conn.commit()
                else:
                    prior = select_result[2] * num_submitted
                    new_avg = (prior + payload['memory_usage'])/(num_submitted+1)
                    set_query = update_clause + 'memoryUsage = ' + str(new_avg) + where_clause
                    cursor.execute(set_query)
                    self.conn.commit()

            if 'timestamps' in payload:
                times_json = json.loads(payload['timestamps'])
                if 'jiff_server_launched' in times_json:
                    start = times_json['jiff_server_launched']
                else:
                    start = times_json['service_ip_retrieved']

                remaining_keys = ['exchanged_ips', 'built_specs_configs', 'launched_config', 'launched_pod', 'pod_succeeded', 'workflow_stopped']
                end = ''
                for k in remaining_keys:
                    if times_json[k] is not None:
                        end = times_json[k]
                if end != '':
                    diff = timestamp_difference(start, end, '%H:%M:%S')
                else:
                    diff = ''
                set_query = update_clause + 'runTime = ' + str(diff) + where_clause
                cursor.execute(set_query)
                self.conn.commit()

            update_submitted = update_clause + 'submittedStats = ' + str(num_submitted+1) + where_clause
            cursor.execute(update_submitted)
            self.conn.commit()
            cursor.close()
            return 'successful'

        else:
            raise Exception("Workflow name missing from payload")

    def get_storage_relationship_from_dataset_id(self, datasetId):
        """
            This function will search the storage relationship table by datasetId and return the result
            params:
                datasetId
        """

        query = 'SELECT * from ' + self.database_name + '.storageRelationships WHERE datasetId="' + datasetId + '"'
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = list(cursor.fetchall())
        cursor.close()

        return result

    def get_cardinal_ips_from_ids(self, cardinalIds):
        """
            This function will return cardinal ips from a list of cardinal ids by searching the database
            params:
                cardinalIds: list of cardinal ids
            returns:
                list of cardinal ips
        """

        query = 'Select cardinalId,cardinalIp from ' + self.database_name + '.cardinals where cardinalId in ' + '(' + ','.join(['%s']*len(cardinalIds)) + ')'
        cursor = self.conn.cursor()
        cursor.execute(query, cardinalIds)
        query_output = list(cursor.fetchall())
        id_ip_dict = {}
        for tpl in query_output:
            id_ip_dict[tpl[0]] = tpl[1]

        result = []
        for id in cardinalIds:
            result.append(id_ip_dict[id])

        cursor.close()

        return result

    def get_workflow_location_from_request(self, dataset_id,operation_name):
        """
            This function will return workflow bucket and key from dataset id and operation
            params:
                dataset_id: dataset id
                operation_name: name of operation
            returns:
                workflow_source_bucket, workflow_source_key
        """

        query = 'Select sourceBucket,sourceKey from ' + self.database_name + '.workflows where datasetId="' + dataset_id + '" and operationName= "' + operation_name+ '"'
        cursor = self.conn.cursor()
        cursor.execute(query)
        query_output = list(cursor.fetchall())[0]
        cursor.close()

        return query_output

    def get_dataset_parameters_from_dataset_id(self, dataset_id):
        """
            This function will return dataset bucket and key from dataset id for all parties
            params:
                dataset_id: dataset id
            returns:
                list of tuples of (parameters)
        """

        query = 'Select parameters from ' + self.database_name + '.datasets where datasetId="' + dataset_id + '"'
        cursor = self.conn.cursor()
        cursor.execute(query)
        query_output = list(cursor.fetchall())[0][0]
        cursor.close()

        return query_output

    # chamberlain db crud operation functions

    # workflow
    def insert_workflow(self, payload):
        """
            This function inserts workflow in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        cols = ['workflowId','operationName', 'datasetId', 'sourceBucket','sourceKey','description']
        identifier_str = '(' + ','.join(['%s' for i in range(len(cols))]) + ')'
        columns_str = '(' + ','.join(cols) + ')'

        flag = all([True for col in cols if col in payload])
        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO ' + self.database_name + '.workflows ' + columns_str + ' VALUES ' + identifier_str
            values_tuple = tuple([payload[col] for col in cols])
            cursor.execute(query, values_tuple)
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            raise Exception("request format not correct")

    def get_workflows(self):
        """
            This function returns workflow in the MySQL chamberlain database
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.workflows'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def get_workflow_id(self, id):
        """
            This function returns workflow with specified in from the MySQL chamberlain database
            params:
                id: id of workflow - string
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.workflows WHERE workflowId="' + str(id) + '"'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def delete_workflow(self, id):
        """
            This function deletes workflow with specified in from the MySQL chamberlain database
            params:
                id: id of workflow - string
        """

        cursor = self.conn.cursor()
        query = 'DELETE FROM ' + self.database_name + '.workflows WHERE workflowId="' + str(id) + '"'
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

        return 'successful'

    def modify_workflow(self, payload):
        """
            This function modifies workflow in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'workflowId' in payload:
            cursor = self.conn.cursor()
            attributes = ['operationName','datasetId', 'sourceBucket','sourceKey','description']
            query = 'UPDATE ' + self.database_name + '.workflows SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where workflowId="' + payload['workflowId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            raise Exception("request format not correct")

    # dataset
    def insert_dataset(self, payload):
        """
            This function inserts dataset in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        cols = ['datasetId', 'datasetSchema','backend','parameters','description']
        identifier_str = '(' + ','.join(['%s' for i in range(len(cols))]) + ')'
        columns_str = '(' + ','.join(cols) + ')'

        flag = all([True for col in cols if col in payload])
        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO ' + self.database_name + '.datasets ' + columns_str + ' VALUES ' + identifier_str
            values_tuple = tuple([payload[col] for col in cols])
            cursor.execute(query, values_tuple)
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            raise Exception("request format not correct")

    def get_datasets(self):
        """
            This function returns dataset in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.datasets'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def get_dataset_id(self, id):
        """
            This function returns dataset with specified in from the MySQL chamberlain database
            params:
                id: id of dataset - string
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.datasets WHERE datasetId="' + str(id) + '"'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def delete_dataset(self, id):
        """
            This function deletes dataset with specified in from the MySQL chamberlain database
            params:
                id: id of dataset - string
        """

        cursor = self.conn.cursor()
        query = 'DELETE FROM ' + self.database_name + '.datasets WHERE datasetId="' + str(id) + '"'
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

        return 'successful'

    def modify_dataset(self, payload):
        """
            This function modifies dataset in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'datasetId' in payload:
            cursor = self.conn.cursor()
            attributes = ['pid','datasetSchema','backend','parameters','description']
            query = 'UPDATE ' + self.database_name + '.datasets SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where datasetId="' + payload['datasetId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            raise Exception("request format not correct")

    # cardinal
    def insert_cardinal(self, payload):
        """
            This function inserts cardinal in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        cols = ['cardinalId', 'cardinalIp','description']
        identifier_str = '(' + ','.join(['%s' for i in range(len(cols))]) + ')'
        columns_str = '(' + ','.join(cols) + ')'

        flag = all([True for col in cols if col in payload])
        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO ' + self.database_name + '.cardinals ' + columns_str + ' VALUES ' + identifier_str
            values_tuple = tuple([payload[col] for col in cols])
            cursor.execute(query, values_tuple)
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            raise Exception("request format not correct")

    def get_cardinals(self):
        """
            This function returns cardinal in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.cardinals'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def get_cardinal_id(self, id):
        """
            This function returns cardinal with specified in from the MySQL chamberlain database
            params:
                id: id of cardinal - string
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.cardinals WHERE cardinalId="' + str(id) + '"'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def delete_cardinal(self, id):
        """
            This function deletes cardinal with specified in from the MySQL chamberlain database
            params:
                id: id of cardinal - string
        """

        cursor = self.conn.cursor()
        query = 'DELETE FROM '  + self.database_name + '.cardinals WHERE cardinalId="' + str(id) + '"'
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

        return 'successful'

    def modify_cardinal(self, payload):
        """
            This function modifies cardinal in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'cardinalId' in payload:
            cursor = self.conn.cursor()
            attributes = ['cardinalIp']
            query = 'UPDATE ' + self.database_name + '.cardinals SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where cardinalId="' + payload['cardinalId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            raise Exception("request format not correct")

    # workflow relationship
    def insert_workflow_relationship(self, payload):
        """
            This function inserts workflow relationship in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        cols = ['workflowRelationshipId', 'datasetId','workflowId','description']
        identifier_str = '(' + ','.join(['%s' for i in range(len(cols))]) + ')'
        columns_str = '(' + ','.join(cols) + ')'

        flag = all([True for col in cols if col in payload])
        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO ' + self.database_name + '.workflowRelationships ' + columns_str + ' VALUES ' + identifier_str
            values_tuple = tuple([payload[col] for col in cols])
            cursor.execute(query, values_tuple)
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            raise Exception("request format not correct")

    def get_workflow_relationships(self):
        """
            This function returns workflow_relationship in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.workflowRelationships'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def get_workflow_relationship_id(self, id):
        """
            This function returns workflow_relationship with specified in from the MySQL chamberlain database
            params:
                id: id of cardinal - string
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.workflowRelationships WHERE workflowRelationshipId="' + str(id) + '"'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def delete_workflow_relationship(self, id):
        """
            This function deletes workflow_relationship with specified in from the MySQL chamberlain database
            params:
                id: id of cardinal - string
        """

        cursor = self.conn.cursor()
        query = 'DELETE FROM ' + self.database_name + '.workflowRelationships WHERE workflowRelationshipId="' + str(id) + '"'
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

        return 'successful'

    def modify_workflow_relationship(self, payload):
        """
            This function modifies worflow relationship in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'workflowRelationshipId' in payload:
            cursor = self.conn.cursor()
            attributes = ['datasetId','workflowId','description']
            query = 'UPDATE ' + self.database_name + '.workflowRelationships SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where workflowRelationshipId="' + payload['workflowRelationshipId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            raise Exception("request format not correct")

    # storage relationship
    def insert_storage_relationship(self, payload):
        """
            This function inserts storage relationship in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """
        cols = ['datasetId', 'cardinals', 'description']
        identifier_str = '(' + ','.join(['%s' for i in range(len(cols))]) + ')'
        columns_str = '(' + ','.join(cols) + ')'

        flag = all([True for col in cols if col in payload])
        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO ' + self.database_name + '.storageRelationships ' + columns_str + ' VALUES ' + identifier_str
            values_tuple = tuple([payload[col] for col in cols])
            cursor.execute(query, values_tuple)
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            raise Exception("request format not correct")

    def get_storage_relationships(self):
        """
            This function returns storage_relationship in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.storageRelationships'
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def get_storage_relationship_id(self, id):
        """
            This function returns storage_relationship with specified in from the MySQL chamberlain database
            params:
                id: id of cardinal - string
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM ' + self.database_name + '.storageRelationships WHERE storageRelationshipId=' + str(id)
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()

        return data

    def delete_storage_relationship(self, id):
        """
            This function deletes storage_relationship with specified in from the MySQL chamberlain database
            params:
                id: id of cardinal - string
        """

        cursor = self.conn.cursor()
        query = 'DELETE FROM ' + self.database_name + '.storageRelationships WHERE storageRelationshipId=' + str(id)
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

        return 'successful'

    def modify_storage_relationship(self, payload):
        """
            This function modifies storage relationship in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'storageRelationshipId' in payload:
            cursor = self.conn.cursor()
            attributes = ['datasetId','cardinals','description']
            query = 'UPDATE ' + self.database_name + '.storageRelationships SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where storageRelationshipId=' + str(payload['storageRelationshipId'])

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            raise Exception("request format not correct")


# helper to find difference between two timestamps
def timestamp_difference(start, end, fmt):
    # fmt = '%Y-%m-%d %H:%M:%S'
    tstamp1 = datetime.strptime(start, fmt)
    tstamp2 = datetime.strptime(end, fmt)

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = round(td.total_seconds() / 60, 4)

    # print('The difference is approx. %s minutes' % td_mins)
    return td_mins
