#!/usr/bin/env python3
"""
End-to-end integration test.
"""

import requests

url = "http://127.0.0.1:5000/"


def register_user(email: str, password: str) -> None:
    """test registration"""
    resp = requests.post(
        url=url+'users', data={'email': email, 'password': password})
    assert resp.json() == {'email': email, 'message': "user created"}
    assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """test login with wrong password"""
    resp = requests.post(url=url+'sessions',
                         data={'email': email, 'password': password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    '''test login with right password'''
    resp = requests.post(url=url+'sessions',
                         data={'email': email, 'password': password})
    assert resp.status_code == 200
    assert resp.json() == {"email": "<user email>", "message": "logged in"}
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """test get /profile route with no session ID"""
    resp = requests.get(url=url+'profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """test get /profile route with session ID"""
    resp = requests.get(url=url+'profile', cookies={"session_id": session_id})
    assert resp.status_code == 200
    assert resp.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """test logout route"""
    resp = requests.delete(
        url=url+'sessions', cookies={"session_id": session_id})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test resetting password using a token"""
    resp = requests.post(url=url+"reset_password", data={"email": email})
    assert resp.status_code == 200
    return resp.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test updating password"""
    resp = requests.put(url=url+"reset_password", data={
                        "email": email,
                        "reset_token": reset_token,
                        "new_password": new_password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
