"""
Quick and simple API for the HeLO-System.
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
from endpoints.teams import Teams

app = Flask(__name__)
api = Api(app)

# add endpoints
api.add_resource(Teams, '/teams')

if __name__ == "__main__":
    app.run()
