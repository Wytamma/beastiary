from fastapi.testclient import TestClient
from .utils import app, headers, hcv_coal_first_sample, ebola_first_sample

client = TestClient(app)


def test_explorer_no_path() -> None:
    response = client.get("/api/explorer/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert "path" in data
    assert "parent" in data
    assert data["path"].endswith("beastiary/backend")
    assert data["parent"].endswith("beastiary")


def test_explorer_with_path() -> None:
    response = client.get("/api/explorer/?path=/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert "path" in data
    assert "parent" in data
    assert data["path"] == "/"
    assert data["parent"] == "/"
