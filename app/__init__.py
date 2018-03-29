from flask import Flask
from config.import Config

app = Flask(_name_)
app.config.from_object(Config)

from app import routes

