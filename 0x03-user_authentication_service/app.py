#!/usr/bin/env python3
"""simple module for starting a flask server"""
from auth import Auth
from flask import Flask, jsonify, request, abort, \
    redirect, url_for


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def hello_world():
    """return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """end-point to register a new user"""

    email, password = request.form.get('email'), request.form.get('password')
    if not email or not password:
        return jsonify({"message": "missing parameters"}), 400

    try:
        usr = AUTH.register_user(email, password)
        return jsonify({'email': usr.email, 'message': "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """create a new session for the user, store it the session ID as a cookie
    """

    email, password = request.form.get('email'), request.form.get('password')
    if not email or not password:
        return jsonify({"message": "missing parameters"}), 400

    IsValidLogin = AUTH.valid_login(email, password)

    if not IsValidLogin:
        abort(401)
    sessionID = AUTH.create_session(email)

    if not sessionID:
        abort(401)

    resp = jsonify({"email": "<user email>", "message": "logged in"})
    resp.set_cookie("sessionID", sessionID)

    return resp


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout function to respond to the DELETE /sessions route.
    """
    session_id = request.cookies.get('session_id', None)

    if not session_id:
        abort(403)
    usr = AUTH.get_user_from_session_id(session_id)

    if not usr:
        abort(403)

    AUTH.destroy_session(usr.id)
    return redirect(url_for("/"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
