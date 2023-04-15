import json
import os
from unittest import TestCase
import uuid
from app.databases import db
from app.models.models import Task, File
from app import app
from flask_jwt_extended import create_access_token

class TestTask(TestCase):
    def setUp(self):
        self.client = app.test_client()   
        additional_claims = {"id": 1}
        self.token = create_access_token(identity=1, additional_claims=additional_claims)        
        

    def tearDown(self):
        tasks = Task.query.all()
        for task in tasks:
            db.session.delete(task)   
        uploads = File.query.all()
        for upload in uploads:
            db.session.delete(upload)   

        db.session.commit()

    def test_get_empty_list(self):      
        endpoint_tasks = "/api/tasks"        
        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())
        self.assertEqual([],result_get_tasks_json)
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_one_element(self):    
        mock_task = self.task_mock(1)  
        endpoint_tasks = "/api/tasks"        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        for result_task in result_get_tasks_json:
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_five_elements(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks"
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        for result_task in result_get_tasks_json:
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        
        self.assertEqual(5,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_max_3_elements(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks?max=3"        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        for result_task in result_get_tasks_json:
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        
        self.assertEqual(3,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_max_3_elements_order_asc_by_default(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks?max=3"        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        increment = 1
        for result_task in result_get_tasks_json:
            self.assertEqual(result_task['id'], str(increment))
            increment = increment + 1
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        

        self.assertEqual(3,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_max_3_elements_order_asc(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks?max=3&order=0"        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        increment = 1
        for result_task in result_get_tasks_json:
            self.assertEqual(result_task['id'], str(increment))
            increment = increment + 1
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        

        self.assertEqual(3,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_elements_order_asc(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks?order=0"    
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        increment = 1
        for result_task in result_get_tasks_json:
            self.assertEqual(result_task['id'], str(increment))
            increment = increment + 1
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        

        self.assertEqual(5,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_elements_order_desc(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks?order=1"        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        increment = len(mock_task)-1
        for result_task in result_get_tasks_json:
            self.assertEqual(result_task['id'], str(increment))
            increment = increment -1
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        

        self.assertEqual(5,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_max_3_elements_order_desc(self):    
        mock_task = self.task_mock(5)  
        endpoint_tasks = "/api/tasks?max=3&order=1"        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())

        increment = len(mock_task)-1
        for result_task in result_get_tasks_json:
            self.assertEqual(result_task['id'], str(increment))
            increment = increment - 1
            for temporal_mock_task in mock_task:
                if result_task['task_id'] == str(temporal_mock_task.task_id):
                    self.assertEqual(result_task['file_name'], temporal_mock_task.file_name)
                    self.assertEqual(result_task['original_extension'], temporal_mock_task.original_extension)
                    self.assertEqual(result_task['new_extension'], temporal_mock_task.new_extension)                    
                    self.assertEqual(result_task['status'], str(temporal_mock_task.status))        

        self.assertEqual(3,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_post_task(self):
        endpoint_tasks = "/api/tasks"        
        self.headers = {'Content-Type': 'multipart/form-data', "Authorization": "Bearer {}".format(self.token)}
        self.archivo = os.path.join(os.path.dirname(__file__), 'test.txt')
        
        with open(self.archivo, 'rb') as f:
            data = {'file': f,'newFormat':'zip'}

            result_get_tasks = self.client.post(endpoint_tasks, headers=self.headers, buffered=True, data=data)
            result_get_tasks_json = json.loads(result_get_tasks.get_data())
            self.assertEqual('uploaded',result_get_tasks_json['status'])
            self.assertEqual(200,result_get_tasks.status_code)

    def test_post_task_without_file(self):
        endpoint_tasks = "/api/tasks"        
        self.headers = {'Content-Type': 'multipart/form-data', "Authorization": "Bearer {}".format(self.token)}
        
        data = {'newFormat':'zip'}

        result_get_tasks = self.client.post(endpoint_tasks, headers=self.headers, buffered=True, data=data)                        
        self.assertEqual(400,result_get_tasks.status_code)

    def test_post_task_without_newFormat(self):
        endpoint_tasks = "/api/tasks"        
        self.headers = {'Content-Type': 'multipart/form-data', "Authorization": "Bearer {}".format(self.token)}
        self.archivo = os.path.join(os.path.dirname(__file__), 'test.txt')
        
        with open(self.archivo, 'rb') as f:
            data = {'file': f}

            result_get_tasks = self.client.post(endpoint_tasks, headers=self.headers, buffered=True, data=data)            
            self.assertEqual(400,result_get_tasks.status_code)

    def test_get_task_by_id(self):
        mock_task = self.task_mock(2)
        id_task = mock_task[0].task_id
        endpoint_tasks = "/api/tasks/"+str(id_task)        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())        
       
        self.assertIsNotNone(result_get_tasks_json['file_name'])
        self.assertIsNotNone(result_get_tasks_json['id'])            
        self.assertIsNotNone(result_get_tasks_json['status'])         
        self.assertEqual(200,result_get_tasks.status_code)

    def test_get_task_by_id_invalid(self):
        self.task_mock(2)
        id_task = 4
        endpoint_tasks = "/api/tasks/"+str(id_task)        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        result_get_tasks_json = json.loads(result_get_tasks.get_data())
        for result_task in result_get_tasks_json:  
            self.assertIsNotNone(result_task['file_name'])
            self.assertIsNotNone(result_task['id'])            
            self.assertIsNotNone(result_task['status']) 
        self.assertEqual(0,len(result_get_tasks_json))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_delete_task_by_id_invalid(self):
        self.task_mock_delete(2)
        id_task = 4
        endpoint_tasks = "/api/tasks/"+str(id_task)        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        result_tasks = Task.query.all()
        self.assertEqual(3,len(result_tasks))
        result_get_tasks = self.client.delete(endpoint_tasks, headers=self.headers)
        
        result_tasks = Task.query.all()
        self.assertEqual(3,len(result_tasks))
        self.assertEqual(200,result_get_tasks.status_code)

    def test_delete_task_by_id(self):
        mock_task = self.task_mock_delete(2)
        
        endpoint_tasks = "/api/tasks/"+str(mock_task[0].task_id)        
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        result_tasks = Task.query.all()
        self.assertEqual(3,len(result_tasks))
        result_get_tasks = self.client.delete(endpoint_tasks, headers=self.headers)
        
        result_tasks = Task.query.all()
        self.assertEqual(2,len(result_tasks))
        self.assertEqual(204,result_get_tasks.status_code)

    
    def task_mock(self, quantity):
        tasks = []    
        for i in range(0, quantity):    
            task_id = str(uuid.uuid4())
            file_name = "myfile"
            original_extension = "pdf"
            new_extension = "zip"
            status = "Uploaded"
            id_user = 1
            new_task = Task(id_user = id_user, task_id=task_id, file_name=file_name, original_extension=original_extension,new_extension=new_extension, status=status)
            tasks.append(new_task)
            db.session.add(new_task)
            db.session.commit()
        
        task_id = str(uuid.uuid4())
        file_name = "myfile"
        original_extension = "pdf"
        new_extension = "zip"
        status = "Uploaded"
        id_user = 2
        new_task = Task(id_user = id_user, task_id=task_id, file_name=file_name, original_extension=original_extension,new_extension=new_extension,status=status)
        tasks.append(new_task)
        db.session.add(new_task)
        db.session.commit()
        
        return tasks
    
    def task_mock_delete(self, quantity):
        tasks = []    
        for i in range(0, quantity):    
            task_id = str(uuid.uuid4())
            file_name = "myfile"
            original_extension = "pdf"
            new_extension = "zip"
            status = "processed"
            id_user = 1
            new_task = Task(id_user = id_user, task_id=task_id, file_name=file_name, original_extension=original_extension,new_extension=new_extension, status=status)
            tasks.append(new_task)
            db.session.add(new_task)
            db.session.commit()
        
        task_id = str(uuid.uuid4())
        file_name = "myfile"
        original_extension = "pdf"
        new_extension = "zip"
        status = "Uploaded"
        id_user = 2
        new_task = Task(id_user = id_user, task_id=task_id, file_name=file_name, original_extension=original_extension,new_extension=new_extension,status=status)
        tasks.append(new_task)
        db.session.add(new_task)
        db.session.commit()
        
        return tasks