from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.databases.database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(128))
    file_name = db.Column(db.String(128))
    original_extension = db.Column(db.String(10))
    id_bucket_original_file = db.Column(db.String(256))
    new_extension = db.Column(db.String(10))
    id_bucket_new_file = db.Column(db.String(256))
    status = db.Column(db.String(10))
    id_user = db.Column(db.Integer)
    file = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable = True)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)    
    task = db.relationship('Task') 

class GetTaskSchema(SQLAlchemyAutoSchema):
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