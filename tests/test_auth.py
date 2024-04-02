import pytest
from flask import g, session, request, url_for
from imgwebapp.db import get_db

def test_index(client,app):
    assert client.get('/').status_code == 200

def test_register(client, app):
    assert client.get('/register').status_code == 302
    response = client.post(
        '/register', data={'reg-username': 'test', 'reg-password': 'test', 'rpt-password':'test'})
    assert response.headers["Location"] == "/"
    assert b'Registration for test is successful!' in client.get('/').data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'rpt_password','message'), (
    ('', '', '', b'Username is required.'),
    ('test', '', '',b'Password is required.'),
    ('test', 'test', 'toast',b'Password is not the same'),
    ('testUser', 'test', 'test',b'User testUser is already registered.'),
))
def test_register_validate_input(client, username, password, rpt_password, message):
    response = client.post(
        '/register',
        data={'reg-username': username, 'reg-password': password, 'rpt-password': rpt_password}
    , follow_redirects=True)
    assert message in response.data

def test_login(client, auth):
    assert client.get('/login').status_code == 302
    response = auth.login()
    assert response.headers["Location"] == '/gallery'

    with client:
        response = client.get('/')
        assert response.status_code == 302
        assert response.headers["Location"] == url_for('gallery')

    with client:
        client.get('/gallery')
        assert session['uid'] == 1
        assert g.user['username'] == 'testUser'

    with client:
        response = auth.login(follow=True)
        assert response.status_code == 200
        assert b'You already logged in!' in response.data
        


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Your username or password is incorrect.'),
    ('testUser', 'a', b'Your username or password is incorrect.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password,True)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    
    with client:
        auth.logout()
        assert 'uid' not in session