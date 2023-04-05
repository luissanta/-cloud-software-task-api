
from unittest import TestCase
from app.databases import db
#from app.models import Task
#from app import app
class TestTask(TestCase):
    def setUp(self):
        #self.client = app.test_client()    
        pass    

    def tearDown(self):
        pass
        #tasks = Task.query.all()
        #for task in tasks:
        #    db.session.delete(task)     

        #db.session.commit()

    def test_get_empty_list(self):
        pass
        #endpoint_tasks = "/api/tasks" #+ str(id_rutina)
        #self.token = ""
        #self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        #result_get_tasks = self.client.get(endpoint_tasks, headers=self.headers)
        #self.assertEqual(200,result_get_tasks.status_code)