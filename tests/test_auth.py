import pytest
from flask import g, session
from JustinWCainPortfolio.db import get_db
import re


def test_login(client, auth):
    assert client.get('/login', follow_redirects=True).status_code == 200
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

@pytest.mark.parametrize('path', (
    '/auth/changepassword',
))
def test_login_required(client, auth, path):
    auth.logout()
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"

@pytest.mark.parametrize('path', (
    '/auth/changepassword',
))
def test_login_access(client, auth, path):
    auth.login()
    response = client.get(path)
    assert not hasattr(response, "Location")

@pytest.mark.parametrize(('currentpassword','newpassword', 'confirmpassword', 'message'), (
    ('adminpass', 'newpass', 'newpass', 'Redirecting...'), #Successfull change causes a redirect to index
    ('adminpass', 'newpass', 'newpass123', 'New passwords do not match.'),
    ('fakepassword', 'newpass', 'newpass', 'Incorrect password.'),
    ('fakepassword', 'newpass', 'newpass123', 'Incorrect password.'),
))
def test_changepassword(client, auth, currentpassword, newpassword, confirmpassword, message):
    auth.login()
    response = client.post('/auth/changepassword',
        data={'current_password': currentpassword, 'new_password' : newpassword, 'confirm_password' : confirmpassword}
    )
    assert re.search(message, response.get_data(as_text=True))

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session