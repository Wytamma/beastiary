from fastapi.testclient import TestClient
from .utils import (
    app,
    headers,
    hcv_coal_first_sample,
    ebola_first_sample,
    csv_first_sample,
)
from beastiary import crud
from beastiary.schemas import TraceCreate
from beastiary.api.core import get_headers


client = TestClient(app)

path = "tests/data/hcv_coal.log"
last_byte, headers_line = get_headers(path=path)

trace = crud.trace.create(
    client.app.db,
    obj_in=TraceCreate(path=path),
    headers_line=headers_line,
    last_byte=last_byte,
)

path = "tests/data/prior.ebola.log"
last_byte, headers_line = get_headers(path=path)

na_trace = crud.trace.create(
    client.app.db,
    obj_in=TraceCreate(path=path),
    headers_line=headers_line,
    last_byte=last_byte,
)

path = "tests/data/beast1.csv"
last_byte, headers_line = get_headers(path=path, delimiter=",")

csv_trace = crud.trace.create(
    client.app.db,
    obj_in=TraceCreate(path=path, delimiter=","),
    headers_line=headers_line,
    last_byte=last_byte,
)


def test_no_trace() -> None:
    response = client.get("/api/traces/100/samples", headers=headers)
    assert response.status_code == 404


def test_get_sample() -> None:
    response = client.get(f"/api/traces/{trace['id']}/samples", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["trace_id"] == trace["id"]
    assert json[0]["data"] == hcv_coal_first_sample


def test_get_sample_limit() -> None:
    response = client.get(f"/api/traces/{trace['id']}/samples?limit=1", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    response = client.get(
        f"/api/traces/{trace['id']}/samples?limit=1000000", headers=headers
    )
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1001


def test_get_samples_with_missing_values() -> None:
    response = client.get(f"/api/traces/{na_trace['id']}/samples", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["trace_id"] == na_trace["id"]
    assert json[0]["data"] == ebola_first_sample


def test_get_csv_sample() -> None:
    response = client.get(f"/api/traces/{csv_trace['id']}/samples", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["trace_id"] == csv_trace["id"]
    print(json[0]["data"])
    assert json[0]["data"] == csv_first_sample
