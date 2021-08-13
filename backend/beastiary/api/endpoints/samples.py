from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from uvicorn.main import run

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


def read_lines(trace, starting_byte):
    with open(trace.path, "r") as f:
        f.seek(starting_byte, 0)
        lines = f.readlines()
        if lines:
            last_byte = f.tell() + 2
        else:
            last_byte = starting_byte
        return last_byte, lines


def lines_to_SampleCreate(headers, lines):
    samples = []
    for line in lines:
        if not line:
            # blank lines are bag...
            # you'll have to have a smart way to handel this with the byte offset
            raise ValueError("Poorly formated line.")
        sample = {}
        data = {key: float(value) for key, value in zip(headers, line.split())}
        sample["data"] = data
        sample["state"] = data["state"]
        samples.append(schemas.sample.SampleCreate(**sample))
    return samples


def check_for_new_samples(db, trace, starting_byte):
    last_byte, lines = read_lines(trace, starting_byte=starting_byte)
    in_samples = lines_to_SampleCreate(trace.headers_line.split(), lines)
    if in_samples:
        crud.sample.create_multi_with_trace(
            db, objs_in=in_samples, trace_id=trace.id, last_row_byte=last_byte
        )


@router.get("/", response_model=List[schemas.Sample])
def get_samples(
    trace_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve samples.
    """
    trace = crud.trace.get(db, trace_id)
    if not trace:
        raise HTTPException(404, "Trace not found!")

    samples = crud.sample.get_multi_by_trace(
        db, trace_id=trace.id, skip=skip, limit=limit
    )

    if len(samples) < limit:
        # check for new samples
        if len(samples) == 0:
            starting_byte = trace.first_byte
        else:
            starting_byte = samples[-1].row_byte
        try:
            check_for_new_samples(db, trace=trace, starting_byte=starting_byte)
        except Exception as e:
            raise e
        # get samples
        samples = crud.sample.get_multi_by_trace(
            db, trace_id=trace.id, skip=skip, limit=limit
        )

    return samples
