from fastapi.testclient import TestClient
from .utils import app, headers, headers_line, last_byte, first_sample
from beastiary import crud
from beastiary.schemas import TraceCreate, sample
from beastiary.db.session import SessionLocal
from beastiary.db.init_db import init_db

db = SessionLocal()
init_db(db)

client = TestClient(app)
trace = crud.trace.create(
    db,
    obj_in=TraceCreate(path="tests/data/hcv_coal.log"),
    headers_line=headers_line,
    last_byte=last_byte,
)


def test_read_no_trace_id():
    response = client.get("/api/samples/", headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "trace_id"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_no_trace():
    response = client.get("/api/samples/?trace_id=100", headers=headers)
    assert response.status_code == 404


def test_get_sample():
    response = client.get("/api/samples/?trace_id=1", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["trace_id"] == trace.id
    assert json[0]["data"] == first_sample["data"]


def test_get_sample_limit():
    response = client.get("/api/samples/?trace_id=1&limit=1", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    response = client.get("/api/samples/?trace_id=1&limit=1000000", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1001
