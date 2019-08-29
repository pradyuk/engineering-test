from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask.cli import FlaskGroup
from project import app, Properties, Points
import os

cli = FlaskGroup(app)
api = Api(app)
app_settings = os.getenv('APP_SETTINGS')  # new
app.config.from_object(app_settings) 

if __name__ == "__main__":
	print("Connected to database.")
	Points.check()
	cli()