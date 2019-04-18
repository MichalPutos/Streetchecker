from flask import Flask, request, render_template, make_response, jsonify
from flask_restful import Resource, Api
from street_check import StreetCheck as StrC

application = app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'), headers)


class Check(Resource):
    def get(self, street):
        sc = StrC()
        result = (sc.main(street))
        return jsonify(results=result)


api.add_resource(Home, '/', '/sc/', )
api.add_resource(Check, '/sc/<string:street>')

if __name__ == '__main__':
    app.run(debug=True)
