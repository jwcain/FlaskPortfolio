import pytest
from flask import g, session
from JustinWCainPortfolio.db import get_db


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'admin'


@pytest.mark.parametrize(('password', 'message'), (
    ('WrongPassword', b'Incorrect password.'),
))
def test_login_validate_input(auth, password, message):
    response = auth.login(password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session