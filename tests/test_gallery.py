import pytest
from flask import g, session, request, url_for
from imgwebapp.db import get_db

def test_gallery(client,app):
    assert client.get('/gallery').status_code == 302
