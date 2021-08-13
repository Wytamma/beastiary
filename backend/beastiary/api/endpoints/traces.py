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
        first_byte, headers = get_headers(trace_in.path)
    except FileNotFoundError as e:
        raise HTTPException(404, detail=e.strerror)
    headers = headers.split()
    headers[0] = "state"
    headers_line = " ".join(headers)
    trace = crud.trace.create(
        db=db, obj_in=trace_in, headers_line=headers_line, first_byte=first_byte
    )
    return trace
