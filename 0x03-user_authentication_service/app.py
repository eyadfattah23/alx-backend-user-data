#!/usr/bin/env python3
"""simple module for starting a flask server"""
from auth import Auth
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    """return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """end-point to register a user"""
    AUTH = Auth()

    email, password = request.form.get('email'), request.form.get('password')
    if not email or not password:
        return jsonify({"message": "missing parameters"}), 400

    try:
        usr = AUTH.register_user(email, password)
        return jsonify({'email': usr.email, 'message': "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
