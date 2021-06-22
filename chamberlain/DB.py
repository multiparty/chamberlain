import time
import mysql.connector
from dotenv import load_dotenv
import os


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
        except Exception as e:
            print(e)

    def retrieve(self, key: str, delay: float = 0.0):
        if delay > 0.0:
            time.sleep(delay)

        storage_relationship = self.get_storage_relationship_from_dataset_id(key)
        cardinalIds = list(storage_relationship[0][2:5])
        cardinalIps = self.get_cardinal_ips_from_ids(cardinalIds)
        owners = ['http://' + ip if 'http://' not in ip else ip for ip in cardinalIps]
        owners = [(i+1, ip) for i, ip in enumerate(owners)]

        return owners

    def get_storage_relationship_from_dataset_id(self, datasetId):
        """
            This function will search the storage relationship table by datasetId and return the result
            params:
                datasetId
        """

        query = 'SELECT * from chamberlain.storagerelationships WHERE datasetId="' + datasetId + '"'
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

        query = 'Select cardinalId,cardinalIp from chamberlain.cardinals where cardinalId in ' + '(' + ','.join(['%s']*len(cardinalIds)) + ')'
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

    # chamberlain db crud operation functions

    # workflow
    def insert_workflow(self, payload):
        """
            This function inserts workflow in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'operationName' in payload and 'workflowId' in payload:
            cursor = self.conn.cursor()
            query = 'INSERT INTO chamberlain.workflows (workflowId,operationName) VALUES (%s,%s)'
            cursor.execute(query, (payload['workflowId'], payload['operationName']))
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            return "request format not correct"

    def get_workflows(self):
        """
            This function returns workflow in the MySQL chamberlain database
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM chamberlain.workflows'
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
        query = 'SELECT * FROM chamberlain.workflows WHERE workflowId="' + str(id) + '"'
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
        query = 'DELETE FROM chamberlain.workflows WHERE workflowId="' + str(id) + '"'
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
            attributes = ['operationName']
            query = 'UPDATE chamberlain.workflows SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where workflowId="' + payload['workflowId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            return "request format not correct"

    # dataset
    def insert_dataset(self, payload):
        """
            This function inserts dataset in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'datasetSchema' in payload and 'datasetId' in payload:
            cursor = self.conn.cursor()
            query = 'INSERT INTO chamberlain.datasets (datasetId,datasetSchema) VALUES (%s,%s)'
            cursor.execute(query, (payload['datasetId'], payload['datasetSchema']))
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            return "request format not correct"

    def get_datasets(self):
        """
            This function returns dataset in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM chamberlain.datasets'
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
        query = 'SELECT * FROM chamberlain.datasets WHERE datasetId="' + str(id) + '"'
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
        query = 'DELETE FROM chamberlain.datasets WHERE datasetId="' + str(id) + '"'
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
            attributes = ['datasetSchema']
            query = 'UPDATE chamberlain.datasets SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where datasetId="' + payload['datasetId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            return "request format not correct"

    # cardinal
    def insert_cardinal(self, payload):
        """
            This function inserts cardinal in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'cardinalIp' in payload and 'cardinalId' in payload:
            cursor = self.conn.cursor()
            query = 'INSERT INTO chamberlain.cardinals (cardinalId,cardinalIp) VALUES (%s,%s)'
            cursor.execute(query, (payload['cardinalId'], payload['cardinalIp']))
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            return "request format not correct"

    def get_cardinals(self):
        """
            This function returns cardinal in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM chamberlain.cardinals'
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
        query = 'SELECT * FROM chamberlain.cardinals WHERE cardinalId="' + str(id) + '"'
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
        query = 'DELETE FROM chamberlain.cardinals WHERE cardinalId="' + str(id) + '"'
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
            query = 'UPDATE chamberlain.cardinals SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where cardinalId="' + payload['cardinalId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            return "request format not correct"

    # workflow relationship
    def insert_workflow_relationship(self, payload):
        """
            This function inserts workflow relationship in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """

        if 'workflowRelationshipId' in payload and 'datasetId' in payload and 'workflowId' in payload and 'columns' in payload:
            cursor = self.conn.cursor()
            query = 'INSERT INTO chamberlain.workflowrelationships (workflowRelationshipId,datasetId,workflowId,columns) VALUES (%s,%s,%s,%s)'
            cursor.execute(query, (payload['workflowRelationshipId'], payload['datasetId'], payload['workflowId'], payload['columns']))
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            return "request format not correct"

    def get_workflow_relationships(self):
        """
            This function returns workflow_relationship in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM chamberlain.workflowrelationships'
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
        query = 'SELECT * FROM chamberlain.workflowrelationships WHERE workflowRelationshipId="' + str(id) + '"'
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
        query = 'DELETE FROM chamberlain.workflowrelationships WHERE workflowRelationshipId="' + str(id) + '"'
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
            attributes = ['datasetId','workflowId','columns']
            query = 'UPDATE chamberlain.workflowRelationships SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where workflowRelationshipId="' + payload['workflowRelationshipId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            return "request format not correct"

    # storage relationship
    def insert_storage_relationship(self, payload):
        """
            This function inserts storage relationship in the MySQL chamberlain database
            params:
                payload: request payload  - dict
        """
        cols = ['storageRelationshipId', 'datasetId', 'cardinalId1', 'cardinalId2', 'cardinalId3']
        flag = all([True for col in cols if col in payload])
        if flag:
            cursor = self.conn.cursor()
            query = 'INSERT INTO chamberlain.storagerelationships (storageRelationshipId,datasetId,cardinalId1,cardinalId2,cardinalId3) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(query, (payload['storageRelationshipId'], payload['datasetId'], payload['cardinalId1'], payload['cardinalId2'], payload['cardinalId3']))
            self.conn.commit()
            cursor.close()

            return 'successfull'
        else:
            return "request format not correct"

    def get_storage_relationships(self):
        """
            This function returns storage_relationship in the MySQL chamberlain database
            params:
        """

        cursor = self.conn.cursor()
        query = 'SELECT * FROM chamberlain.storagerelationships'
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
        query = 'SELECT * FROM chamberlain.storagerelationships WHERE storageRelationshipId="' + str(id) + '"'
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
        query = 'DELETE FROM chamberlain.storagerelationships WHERE storageRelationshipId="' + str(id) + '"'
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
            attributes = ['datasetId','cardinalId1','cardinalId2','cardinalId3']
            query = 'UPDATE chamberlain.storageRelationships SET '
            for key,value in payload.items():
                if key in attributes :
                    query += key + '="' + value + '", '

            query = query[:-2] + 'where storageRelationshipId="' + payload['storageRelationshipId'] + '"'

            cursor.execute(query)
            self.conn.commit()
            cursor.close()

            return 'successfull'

        else:
            return "request format not correct"
