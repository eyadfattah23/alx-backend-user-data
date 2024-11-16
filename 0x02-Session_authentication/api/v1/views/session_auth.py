#!/usr/bin/env python3
""" Module handle all routes for the Session authentication.
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User instance based on the email
    """
    email, password = request.form.get('email'), request.form.get('password')

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users_list = User.search({"email": email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404

    if not users_list:
        return jsonify({"error": "no user found for this email"}), 404

    usr = users_list[0]
    if usr.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(usr.id)
        response = jsonify(usr.to_json())
        try:
            response.set_cookie(getenv('SESSION_NAME'), session_id)
        except Exception as e:
            return None
        return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def user_logout() -> str:
    """ deletes the user session / logout
    """
    from api.v1.app import auth

    logout_success = auth.destroy_session(request)

    if not logout_success:
        abort(404)

    else:
        return jsonify({}), 200
