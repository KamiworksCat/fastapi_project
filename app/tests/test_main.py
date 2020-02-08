from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.json() == {"msg": "Hello World"}
    assert response.status_code == 200
