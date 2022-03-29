from beastiary.api.core import add_trace
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request

from beastiary import crud, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Trace])
def get_traces(
    request: Request,
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.Trace]:
    """
    Retrieve traces.
    """
    traces = crud.trace.get_multi(db=request.app.db, skip=skip, limit=limit)
    return traces


@router.get("/{trace_id}", response_model=schemas.Trace)
def get_trace(request: Request, trace_id: int) -> dict:
    """
    Retrieve traces.
    """
    trace = crud.trace.get(db=request.app.db, id=trace_id)
    if not trace:
        raise HTTPException(404, "Trace not found!")
    return trace


@router.post("/", response_model=schemas.Trace)
def create_trace(
    request: Request,
    *,
    trace_in: schemas.TraceCreate,
) -> dict:
    """
    Create new trace.
    """
    try:
        trace = add_trace(request.app.db, trace_in)
    except FileNotFoundError as e:
        raise HTTPException(404, detail="Could not find log file!")
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(500, detail=f"Could not add {trace_in.path}")
    return trace
