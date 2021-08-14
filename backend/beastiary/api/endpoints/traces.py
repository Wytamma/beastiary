from beastiary.schemas import sample
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Trace])
def get_traces(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve traces.
    """
    traces = crud.trace.get_multi(db=db, skip=skip, limit=limit)
    return traces


@router.get("/{trace_id}", response_model=schemas.Trace)
def get_trace(trace_id, db: Session = Depends(deps.get_db)) -> Any:
    """
    Retrieve traces.
    """
    trace = crud.trace.get(db=db, id=trace_id)
    if not trace:
        raise HTTPException(404, "Trace not found!")
    return trace


def get_headers(path):
    with open(path, "r") as f:
        headers_set = False
        while True:
            line = f.readline()
            if line.startswith("#"):
                continue
            return f.tell(), line


@router.post("/", response_model=schemas.Trace)
def create_trace(
    *,
    db: Session = Depends(deps.get_db),
    trace_in: schemas.TraceCreate,
) -> Any:
    """
    Create new trace.
    """
    # get headers
    try:
        last_byte, headers = get_headers(trace_in.path)
    except FileNotFoundError as e:
        raise HTTPException(404, detail="Could not find log file!")
    headers = headers.split()
    headers[0] = "state"
    headers_line = " ".join(headers)
    trace = crud.trace.create(
        db=db, obj_in=trace_in, headers_line=headers_line, last_byte=last_byte
    )
    return trace
