from ..databases.database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(128))
    original_extension = db.Column(db.String(10))
    id_bucket_original_file = db.Column(db.String(256))
    newExtension = db.Column(db.String(10))
    id_bucket_new_file = db.Column(db.String(256))
    status = db.Column(db.String(10))