"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


@app.route('/members', methods=["POST"])
def add_member():
    request_body = request.json
    data = {
        "first_name": request_body["first_name"],
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }
    jackson_family.add_member(data)
    members = jackson_family.get_all_members()
    print(members)
    return jsonify(members), 200


@app.route('/members/<int:id>', methods=["GET"])
def get_member(id):
    return jsonify(jackson_family.get_member(id)), 200


@app.route('/members/<int:id>', methods=["DELETE"])
def delete_member(id):
    return jsonify(jackson_family.delete_member(id)), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


"""
[{'id': 1,
'first_name': 'John',
'last_name': 'Jackson',
'age': 33,
'lucky_numbers': [7, 13, 22]},
{'id': 2, 'first_name':
'Jane', 'last_name':
'Jackson', 'age': 35,
'lucky_numbers': [10, 14, 3]},
{'id': 3,
'first_name': 'Jimmy',
'last_name': 'Jackson',
'age': 5,
'lucky_numbers': [1]},
{'first_name': 'chanchito',
'age': 33,
'lucky_numbers': [7, 13, 22],
'id': <bound method FamilyStructure._generate_id of <datastructures.FamilyStructure object at 0x72f3e6e63770>>, 'last_name': 'Jackson'}]
"""
