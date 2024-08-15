#!/usr/bin/env python3
"""
Main file
"""
import requests

host = "http://127.0.0.1:5000/{}"


def register_user(email: str, password: str) -> None:
    """ integration test for  correct user registeration"""
    url = host.format('users')

    data = {'email': email, 'password': password}
    r = requests.post(url, data=data)

    expected = {"email": email, "message": "user created"}

    assert r.json() == expected
    assert r.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ integration test for login with incorect pass"""
    url = host.format('sessions')

    data = {'email': email, 'password': password}
    r = requests.post(url, data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ integration test for  log in correct creds"""
    url = host.format('sessions')

    data = {'email': email, 'password': password}
    r = requests.post(url, data=data)

    expected = {"email": email, "message": "logged in"}

    assert r.status_code == 200
    assert r.json() == expected

    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """ integration test for profile not loged in"""
    url = host.format('profile')

    r = requests.get(url)

    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ integration test for profile with session id"""
    url = host.format('profile')

    cookies = dict(session_id=session_id)
    r = requests.get(url, cookies=cookies)

    expected = {"email": "guillaume@holberton.io"}

    assert r.status_code == 200
    assert r.json() == expected


def log_out(session_id: str) -> None:
    """ integration test for loging out and redirect"""
    url = host.format('sessions')

    cookies = dict(session_id=session_id)
    r = requests.delete(url, cookies=cookies)

    expected = {"message": "Bienvenue"}

    assert r.history[0].status_code == 302
    assert r.status_code == 200
    assert r.json() == expected


def reset_password_token(email: str) -> str:
    """ integration test for for reset password route"""
    url = host.format('reset_password')

    data = {'email': email}
    r = requests.post(url, data=data)

    expected = ("email", email)

    assert r.status_code == 200
    assert expected in r.json().items()

    return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ integration test for update pass using restet token"""
    url = host.format('reset_password')

    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put(url, data=data)

    expected = {"email": email, "message": "Password updated"}

    assert r.status_code == 200
    assert expected == r.json()


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
