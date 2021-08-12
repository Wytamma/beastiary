from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from uvicorn.main import run

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


def read_lines(trace, starting_byte, limit=None):
    with open(trace.path, "r") as f:
        f.seek(starting_byte, 0)
        if limit:
            lines = []
            for _ in range(limit):
                lines.append(f.readline())
        else:
            lines = f.readlines()
        if lines:
            last_byte = f.tell() + 2
        else:
            last_byte = starting_byte
        return last_byte, lines


def lines_to_samples(headers, lines, trace_id):
    samples = []
    for line in lines:
        if not line:
            # blank lines are bag...
            # you'll have to have a smart way to handel this with the byte offset
            raise ValueError("Poorly formated line.")
        sample = {}
        data = {key: float(value) for key, value in zip(headers, line.split())}
        sample["data"] = data
        sample["sample"] = data["sample"]
        sample["trace_id"] = trace_id
        samples.append(sample)

    return samples


@router.get("/", response_model=List[schemas.Sample])
def get_samples(
    trace_id: int,
    limit: int = 100,
    get_all: bool = False,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve samples.
    """
    trace = crud.trace.get(db, trace_id)
    if not trace:
        raise HTTPException(404, "Trace not found!")
    current_trace_data = jsonable_encoder(trace)
    trace_in = schemas.TraceUpdate(**current_trace_data)
    if get_all:
        starting_byte = trace.first_byte
    else:
        starting_byte = trace.last_byte
    last_byte, lines = read_lines(trace, starting_byte, limit=limit)
    samples = lines_to_samples(trace.headers_line.split(), lines, trace.id)
    trace_in.last_byte = last_byte
    crud.trace.update(db, db_obj=trace, obj_in=trace_in)
    return samples
