from fastapi.testclient import TestClient
from .utils import app, headers
from beastiary import crud
from beastiary.schemas import TreeCreate
from beastiary.api.core import add_tree

client = TestClient(app)

path = "tests/data/test.trees"


def test_read_wrong_tree_id() -> None:
    response = client.get("/api/trees/42", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Tree not found!"}


def test_get_tree() -> None:
    try:
        crud.tree.remove(db=client.app.db, id=1)
    except:
        pass
    tree = add_tree(client.app.db, TreeCreate(path=path))
    response = client.get(f"/api/trees/{tree['id']}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tree["id"]
    assert data["path"] == str(tree["path"])
    assert data["last_byte"] == tree["last_byte"]


def test_get_trees() -> None:
    add_tree(client.app.db, TreeCreate(path=path))
    add_tree(client.app.db, TreeCreate(path=path))
    add_tree(client.app.db, TreeCreate(path=path))
    response = client.get("/api/trees/", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) >= 3


def test_add_tree() -> None:
    response = client.post("/api/trees/", headers=headers, json={"path": path})
    assert response.status_code == 200
    json = response.json()
    assert json["path"] == path


def test_add_tree_wrong_path() -> None:
    response = client.post(
        "/api/trees/", headers=headers, json={"path": "tests/data/fake.trees"}
    )
    assert response.status_code == 404
    json = response.json()
    assert json["detail"] == "Could not find tree file!"
