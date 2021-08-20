from fastapi.testclient import TestClient
from .utils import app, headers

client = TestClient(app)


def test_read_main() -> None:
    response = client.get("/", headers=headers)
    assert response.status_code == 200


def test_read_token() -> None:
    response = client.get("/api/security/token", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"token": "testing"}


def test_no_security() -> None:
    app.security = False
    client = TestClient(app)
    response = client.get("/api/security/token")
    assert response.status_code == 200
    assert response.json() == {"token": "testing"}
    app.security = True


def test_no_token_fails() -> None:
    response = client.get("/api/security/token")
    assert response.status_code == 401
