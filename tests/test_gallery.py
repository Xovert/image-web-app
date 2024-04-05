import pytest
from flask import g, session, request, url_for
from imgwebapp.db import get_db
from pathlib import Path
from sqlite3 import OperationalError

samples = Path(__file__).parent / "samples"

def test_gallery(client, auth):
    response = client.get('/gallery')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    auth.login()
    response = client.get('/', follow_redirects=True)
    assert b'Upload' in response.data
    assert b'Logout' in response.data

@pytest.mark.parametrize('path', (
    '/upload',
    '/delete/1'
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/"


@pytest.mark.parametrize(('filename, test_code, username, password'), (
        ('burger.jpg', 200, 'testUser', 'usertest'),
        ('football.jpg', 200, 'testUser', 'usertest'),
        ('kitchen.jpg', 200, 'userTwo', 'twouser'),
        ('burger.jpg', 404, 'userTwo', 'twouser')
))
def test_get_file(client, auth, filename, test_code, username, password):
    if username is not None and password is not None:
        response = auth.login(username,password, follow=True)
        assert f'Hello, {username}'.encode('utf-8') in response.data
    assert client.get(f'/uploads/{filename}').status_code == test_code
    

def datas_dict(filename, status_code, message):
    return dict(filename=filename, status_code=status_code, message=message)

@pytest.mark.parametrize(('username, password, datas'),(
        ('testUser', 'usertest', [
            datas_dict('leaves.png', 200, b'Image upload successful!'), 
            datas_dict('lightbulb.jpg', 200, b'Image upload successful!')
        ]),
        ('userTwo', 'twouser', [
            datas_dict('house.jpg', 200, b'Image upload successful!'), 
            datas_dict('birds.jpg', 200, b'Image upload successful!')
        ]),
        ('userTwo', 'twouser', [
            datas_dict('house.jpg', 200, b'Image upload successful!'), 
            datas_dict('house.jpg', 200, b'File already exists!')
        ]),
        ('testUser', 'usertest', [
            datas_dict('hello.py', 404, b'Only images are allowed!'),
            datas_dict(None, 404, b'File upload must not be empty!'),
        ]),
))
def test_upload_image(client, auth, username, password, datas):
    auth.login(username,password)
    for data in datas:
        if data['filename'] is not None:
            response = client.post('/upload', data={
                "photo": ((samples / data['filename']).open("rb"), data['filename']),
            }, follow_redirects=True)
        else:
            response = client.post('/upload', data={}, follow_redirects=True)

        assert response.status_code == 200
        assert response.request.path == '/gallery'
        assert data['message'] in response.data
        test_get_file(client, auth, data['filename'], data['status_code'], None, None)

def test_entity_too_large(client, auth):
    auth.login('userTwo', 'twouser')
    response = client.post('/upload', data={
        "photo": ((samples / 'football.jpg').open("rb"), 'football.jpg'),
        }, follow_redirects=True)
    assert response.request.path == '/gallery'
    assert response.status_code == 200
    assert b'File Cannot Exceed 5.0 MiB'

@pytest.mark.parametrize('path',(
        '/delete/0',
))
def test_exists(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_delete(client, auth, app):
    auth.login('testUser', 'usertest')
    for img_id in [1,2]:
        with app.app_context():
            db = get_db()
            img_name = db.execute('SELECT img_name FROM images where id = ?', (img_id,)).fetchone()
            response = client.post(f'/delete/{img_id}', follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == '/gallery'
            assert b'Image successfully deleted!' in response.data
            assert db.execute('SELECT img_name FROM images WHERE id = ?',(img_id,)).fetchone() is None
            test_get_file(client, auth, img_name, 404, None, None)
    
    # Testing IDOR
    response = client.post(f'/delete/3', follow_redirects=True)
    assert response.status_code == 404
    