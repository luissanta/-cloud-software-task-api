import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET_KEY = 'SFDJKGKJFD7SG987FDS?9889'
    STATIC_FOLDER = "views/static/"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///task.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
