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
    return jsonify(response_body["family"]), 200


@app.route('/members', methods=["POST"])
def add_member():
    request_body = request.json
    response_body = {}
    body = {
        "first_name": str,
        "age": int,
        "lucky_numbers": list
    }
    for propiedad, tipe in body.items():
        if propiedad not in request_body:
            response_body["ERROR"] = f"No se ha encontrado la propiedad {propiedad} en el cuerpo de la solicitud"
            return jsonify(response_body), 400
        if type(request_body[propiedad]) != tipe:
            response_body[
                "ERROR"] = f"La propiedad {propiedad} deberia ser {tipe.__name__} y no {type(request_body[propiedad]).__name__}"
            return jsonify(response_body), 400

    member = jackson_family.add_member(request_body)
    return jsonify(member), 200


@app.route('/members/<int:id>', methods=["GET", "DELETE"])
def get_or_delete(id):
    if request.method == "GET":
        member = jackson_family.get_member(id)
        response = member if member else f"No existe familiar con el id {id}"
        return jsonify(response), 200 if member else 404
    elif request.method == "DELETE":
        response = jackson_family.delete_member(id)
        response_body = {}
        response_body["done"] = response
        return jsonify(response_body), 200 if response_body["done"] else 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
