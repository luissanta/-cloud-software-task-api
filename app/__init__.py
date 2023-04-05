from flask import Flask
from config import ProductionConfig
from flask_cors import CORS
from app.routes import api_routes
from app.databases import db

app = Flask(__name__)
app.config.from_object(ProductionConfig)
app_context = app.app_context()
app_context.push()
cors = CORS(app)

db.init_app(app)
db.create_all()

app.register_blueprint(api_routes, url_prefix='/api')
