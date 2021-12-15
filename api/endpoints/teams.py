"""
Endpoint for the different teams.
"""

from typing_extensions import Required
from flask_restful import Resource, Api, reqparse

class Teams(Resource):

    def get(self):
        parser = reqparse.RequestParser()

        # required arguments for getting a team
        parser.add_argument('name', required=True)

        # parse arguments to dictionary
        args = parser.parse_args()

        # data base stuff
        print(args["name"])

        return "Hello", 200


    def post(self):
        pass


    def put(self):
        pass
