from fastapi.testclient import TestClient
from .utils import app, headers, headers_line, last_byte, first_sample
from beastiary import crud
from beastiary.schemas import TraceCreate, sample
from beastiary.db.session import SessionLocal
from beastiary.db.init_db import init_db

db = SessionLocal()
init_db(db)

client = TestClient(app)


def test_read_wrong_trace_id():
    response = client.get("/api/traces/42", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Trace not found!"}


def test_get_trace():
    try:
        crud.trace.remove(db=db, id=1)
    except:
        pass
    crud.trace.create(
        db,
        obj_in=TraceCreate(path="tests/data/hcv_coal.log"),
        headers_line=headers_line,
        last_byte=last_byte,
    )
    response = client.get("/api/traces/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "path": "tests/data/hcv_coal.log",
        "id": 1,
        "headers_line": "state posterior likelihood prior treeLikelihood TreeHeight freqParameter.1 freqParameter.2 freqParameter.3 freqParameter.4 rateAC rateAG rateAT rateCG rateGT gammaShape BayesianSkyline bPopSizes.1 bPopSizes.2 bPopSizes.3 bPopSizes.4 bGroupSizes.1 bGroupSizes.2 bGroupSizes.3 bGroupSizes.4",
        "last_byte": 6479,
    }


def test_get_trace():
    try:
        crud.trace.remove(db=db, id=1)
    except:
        pass
    crud.trace.create(
        db,
        obj_in=TraceCreate(path="tests/data/hcv_coal.log"),
        headers_line=headers_line,
        last_byte=last_byte,
    )
    crud.trace.create(
        db,
        obj_in=TraceCreate(path="tests/data/hcv_coal.log"),
        headers_line=headers_line,
        last_byte=last_byte,
    )
    crud.trace.create(
        db,
        obj_in=TraceCreate(path="tests/data/hcv_coal.log"),
        headers_line=headers_line,
        last_byte=last_byte,
    )
    response = client.get("/api/traces/", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 3
    for trace in json:
        crud.trace.remove(db=db, id=trace["id"])


def test_add_trace():
    response = client.post(
        "/api/traces/", headers=headers, json={"path": "tests/data/hcv_coal.log"}
    )
    assert response.status_code == 200
    json = response.json()
    assert json["path"] == "tests/data/hcv_coal.log"


def test_add_trace_wrong_path():
    response = client.post(
        "/api/traces/", headers=headers, json={"path": "tests/data/fake.log"}
    )
    assert response.status_code == 404
    json = response.json()
    assert json["detail"] == "Could not find log file!"
