from fastapi.testclient import TestClient
from .utils import app, headers
from beastiary import crud
from beastiary.schemas import TraceCreate
from beastiary.api.core import add_trace

client = TestClient(app)

path = "tests/data/hcv_coal.log"


def test_read_wrong_trace_id() -> None:
    response = client.get("/api/traces/42", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Trace not found!"}


def test_get_trace() -> None:
    try:
        crud.trace.remove(db=client.app.db, id=1)
    except:
        pass
    trace = add_trace(client.app.db, TraceCreate(path=path))
    response = client.get(f"/api/traces/{trace['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "path": path,
        "id": trace["id"],
        "headers_line": "state posterior likelihood prior treeLikelihood TreeHeight freqParameter.1 freqParameter.2 freqParameter.3 freqParameter.4 rateAC rateAG rateAT rateCG rateGT gammaShape BayesianSkyline bPopSizes.1 bPopSizes.2 bPopSizes.3 bPopSizes.4 bGroupSizes.1 bGroupSizes.2 bGroupSizes.3 bGroupSizes.4",
        "last_byte": 6479,
        "delimiter": None,
    }


def test_get_traces() -> None:
    add_trace(client.app.db, TraceCreate(path=path))
    add_trace(client.app.db, TraceCreate(path=path))
    add_trace(client.app.db, TraceCreate(path=path))
    response = client.get("/api/traces/", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) >= 3


def test_add_trace() -> None:
    response = client.post("/api/traces/", headers=headers, json={"path": path})
    assert response.status_code == 200
    json = response.json()
    assert json["path"] == path


def test_add_trace_wrong_path() -> None:
    response = client.post(
        "/api/traces/", headers=headers, json={"path": "tests/data/fake.log"}
    )
    assert response.status_code == 404
    json = response.json()
    assert json["detail"] == "Could not find log file!"


def test_change_delimiter() -> None:
    path = "tests/data/beast1.csv"
    response = client.post(
        "/api/traces/", headers=headers, json={"path": path, "delimiter": ","}
    )
    assert response.status_code == 200
    json = response.json()
    assert json["path"] == path
    assert json["delimiter"] == ","
    assert (
        json["headers_line"]
        == "state,joint,prior,likelihood,treeModel.rootHeight,age(root),treeLength,tmrca(B117),tmrca(B1351),tmrca(P1),tmrca(B16172),age(B117),age(B1351),age(P1),age(B16172),exponential.popSize,exponential.growthRate,gtr.rates.rateAC,gtr.rates.rateAG,gtr.rates.rateAT,gtr.rates.rateCG,gtr.rates.rateCT,gtr.rates.rateGT,alpha,clock.rate,B117.rate,B1351.rate,P1.rate,B16172.rate,meanRate,coefficientOfVariation,covariance,treeLikelihood,branchRates,coalescent"
    )
