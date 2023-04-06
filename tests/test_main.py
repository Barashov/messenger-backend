from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_start_server():
    status = client.get('/hello_world').status_code
    assert status == 404
