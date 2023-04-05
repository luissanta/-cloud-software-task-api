from flask import Flask
from config import DevelopmentConfig
from flask_cors import CORS
from .routes import api_routes
from .databases import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app_context = app.app_context()
app_context.push()
cors = CORS(app)

db.init_app(app)
db.create_all()

app.register_blueprint(api_routes, url_prefix='/api')
