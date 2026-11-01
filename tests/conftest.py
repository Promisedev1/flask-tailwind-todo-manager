import os
from threading import Thread
from werkzeug.serving import make_server

os.environ["TODO_DATABASE_URI"] = "sqlite:///:memory:"

from run import app, db

import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        assert str(db.engine.url) == "sqlite:///:memory:"
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def live_server_url(client):
    server = make_server("127.0.0.1", 0, app)
    thread = Thread(target=server.serve_forever)
    thread.start()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()
    thread.join()