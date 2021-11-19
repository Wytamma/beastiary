from beastiary.api.core import add_trace
from beastiary.models.trace import Trace
from beastiary.schemas import sample
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps
from beastiary.api.core import check_for_new_samples

router = APIRouter()


@router.get("/", response_model=List[schemas.Trace])
def get_traces(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Trace]:
    """
    Retrieve traces.
    """
    traces = crud.trace.get_multi(db=db, skip=skip, limit=limit)
    return traces


@router.get("/{trace_id}", response_model=schemas.Trace)
def get_trace(trace_id: int, db: Session = Depends(deps.get_db)) -> Trace:
    """
    Retrieve traces.
    """
    trace = crud.trace.get(db=db, id=trace_id)
    if not trace:
        raise HTTPException(404, "Trace not found!")
    return trace


@router.post("/", response_model=schemas.Trace)
def create_trace(
    *,
    db: Session = Depends(deps.get_db),
    trace_in: schemas.TraceCreate,
) -> Trace:
    """
    Create new trace.
    """
    try:
        trace = add_trace(db, trace_in)
    except FileNotFoundError as e:
        raise HTTPException(404, detail="Could not find log file!")
    except Exception as e:
        raise HTTPException(500, detail=f"Could not add {trace_in.path}")
    # get samples
    # check_for_new_samples(db, trace=trace)
    return trace
