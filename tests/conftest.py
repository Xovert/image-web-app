import os
import tempfile
from shutil import copyfile

import pytest
from imgwebapp import create_app
from imgwebapp.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    with tempfile.TemporaryDirectory() as tmp_path:
        db_fd, db_path = tempfile.mkstemp(dir=tmp_path)

        app = create_app({
            'TESTING': True,
            'DATABASE': db_path,
            'WTF_CSRF_ENABLED': False,
            'MAX_CONTENT_LENGTH': 5*1024*1024,
        }, instance_path=tmp_path)

        with app.app_context():
            init_db()
            get_db().executescript(_data_sql)

        dir = create_dir(tmp_path, 'testUser')
        assert os.path.isdir(dir) == True
        insert_file(dir, ['burger.jpg','football.jpg'])
        dir = create_dir(tmp_path, 'userTwo')
        assert os.path.isdir(dir) == True
        insert_file(dir, ['kitchen.jpg'])

        yield app

        os.close(db_fd)
        os.unlink(db_path)


def create_dir(tmp_path, usr_path):
    dir_path = os.path.join(tmp_path, 'uploads', usr_path)
    os.makedirs(dir_path)
    return dir_path

def insert_file(dir, files=[]):
    for filename in files:
        filesave = os.path.join(dir,filename)
        copyfile(os.path.join(os.path.dirname(__file__), 'samples', filename),
                 filesave)
        assert os.path.isfile(filesave) == True

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='testUser', password='usertest',follow=False):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password},
            follow_redirects=follow
        )

    def logout(self):
        return self._client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)