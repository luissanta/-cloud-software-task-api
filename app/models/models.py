from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import TIMESTAMP, func
from app.databases.database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(128))
    file_name = db.Column(db.String(128))
    original_extension = db.Column(db.String(10))
    new_extension = db.Column(db.String(10))
    status = db.Column(db.String(10))
    id_user = db.Column(db.Integer)
    id_original_file = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable = True)
    id_converted_file = db.Column(db.Integer)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    created_at = db.Column(TIMESTAMP)
    
    task = db.relationship('Task') 

class GetTaskSchema(Schema):
    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()
    file_name = fields.String()
    original_extension = fields.String()
    new_extension = fields.String()
    status = fields.String()
    task_id = fields.String()

class PostTaskSchema(Schema):
    class Meta:
        model = Task
        include_relationships = False
        include_fk = False
        load_instance = False
        
    id = fields.String()
    status = fields.String()   

class GetTaskByIdSchema(Schema):
    class Meta:
        model = Task
        include_relationships = False
        include_fk = False
        load_instance = False
        
    id = fields.String()
    status = fields.String()   
    file_name = fields.String()   
