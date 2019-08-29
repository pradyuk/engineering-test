from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from flask.cli import FlaskGroup
from datetime import datetime
from sqlalchemy import func
from geoalchemy2 import *
from io import BytesIO
from shapely import wkb
import urllib.request
from PIL import Image
import requests
import json


app = Flask(__name__)

api = Api(app)
db = SQLAlchemy(app)

# sample_data = {
#   "type": "Feature",
#   "geometry": {
# 	"type": "Point",
# 	"coordinates": [125.6, 10.1]
#   },
#   "properties": {
# 	"name": "Dinagat Islands"
#   }
# }
class InsertPoints(db.Model):
	__tablename__ = "pointstable"

	idl = db.Column(db.String(100), primary_key=True)
	longi = db.Column(db.Float)
	lat = db.Column(db.Float)


class Properties(db.Model):
	"""A city, including its geospatial data."""

	__tablename__ = "properties"


	id = db.Column(db.String(100), primary_key=True)
	geocode_geo = db.Column(db.String(100))
	parcel_geo = db.Column(db.String(100))
	building_geo = db.Column(db.String(100))
	image_bounds = db.Column(db.Float)
	image_url = db.Column(db.String(100))


class FindImage(Resource):
	def get(self):
		iden = request.args.get('id')
		property_lst = Properties.query.all()
		for prop in property_lst:
			if prop.id == iden:
				response = requests.get(prop.image_url)
				content = BytesIO(response.content).read()
				return(str(content))
		return "Could not find property"
		content = BytesIO(response.content).read()
		return(str(content))


class Find(Resource):
	@app.route('/findindistance', methods=['GET', 'POST'])
	def fin():
		if request.method=='GET':
			return("Make valid POST request with JSON body and request parameter")
		if request.method=='POST':
			dist = request.args.get('dist')
			sample_data=request.get_json()

			if not sample_data or not isinstance(sample_data,dict):
				return "Invalid payload/JSON object"
			
			points_lst = InsertPoints.query.all()
			geom = sample_data.get("geometry")
			coor = geom.get("coordinates")
			com = "select idl from (SELECT a.idl,ST_DistanceSphere(geometry(point("+str(coor[0])+","+str(coor[1])+")),geometry(point(a.longi, a.lat)) )as abc FROM pointsTable a) a where abc<"+str(dist)+""

			result = db.engine.execute(com)
			row = result.fetchall()
			res_set = []
			for r in range(len(row)):
				res_set.append(row[r][0])
			if res_set:
				return(str(res_set))
			return "no records found withing that distance"
		else:
			return("ok")
		

class Points:
	def check():
		db.create_all()
		db.session.commit()
		property_lst = Properties.query.all()
		for lake in property_lst:
			point = wkb.loads(lake.geocode_geo,hex=True)
			geo = "ST_MakePoint(({} {})".format(point.x, point.y)
			points_lst = InsertPoints.query.all()
			there = 0
			for item in points_lst:
				if(item.idl == lake.geocode_geo):
					there = 1
			if(there==0):
				ins = InsertPoints(idl=lake.geocode_geo, longi=point.x, lat=point.y)
				db.session.add(ins)
				db.session.commit()


api.add_resource(FindImage, '/findimage')
