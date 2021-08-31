from fastapi.testclient import TestClient
from .utils import app, headers, hcv_coal_first_sample, ebola_first_sample
from beastiary import crud
from beastiary.schemas import TraceCreate, sample
from beastiary.db.session import SessionLocal
from beastiary.db.init_db import init_db
from beastiary.api.core import get_headers

db = SessionLocal()
init_db(db)

client = TestClient(app)

path = "tests/data/hcv_coal.log"
last_byte, headers_line = get_headers(path=path)

trace = crud.trace.create(
    db,
    obj_in=TraceCreate(path=path),
    headers_line=headers_line,
    last_byte=last_byte,
)

path = "tests/data/prior.ebola.log"
last_byte, headers_line = get_headers(path=path)

na_trace = crud.trace.create(
    db,
    obj_in=TraceCreate(path=path),
    headers_line=headers_line,
    last_byte=last_byte,
)


def test_read_no_trace_id() -> None:
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


def test_no_trace() -> None:
    response = client.get("/api/samples/?trace_id=100", headers=headers)
    assert response.status_code == 404


def test_get_sample() -> None:
    response = client.get("/api/samples/?trace_id=1", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["trace_id"] == trace.id
    assert json[0]["data"] == hcv_coal_first_sample


def test_get_sample_limit() -> None:
    response = client.get("/api/samples/?trace_id=1&limit=1", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    response = client.get("/api/samples/?trace_id=1&limit=1000000", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1001


def test_get_samples_with_missing_values() -> None:
    response = client.get("/api/samples/?trace_id=2", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["trace_id"] == na_trace.id
    assert json[0]["data"] == ebola_first_sample
