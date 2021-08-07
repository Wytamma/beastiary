from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from uvicorn.main import run

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


def read_lines(run, starting_byte, limit=None):
    with open(run.path, "r") as f:
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


def lines_to_samples(headers, lines, run_id):
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
        sample["run_id"] = run_id
        samples.append(sample)

    return samples


@router.get("/", response_model=List[schemas.Sample])
def get_samples(
    run_id: int,
    limit: int = 100,
    get_all: bool = False,
    uuid: str = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve samples.
    """
    run = crud.run.get(db, run_id)
    if not run:
        raise HTTPException(404, "Run not found!")
    current_run_data = jsonable_encoder(run)
    run_in = schemas.RunUpdate(**current_run_data)
    if get_all:
        starting_byte = run.first_byte
    else:
        starting_byte = run.last_byte
    last_byte, lines = read_lines(run, starting_byte, limit=limit)
    print(last_byte)
    samples = lines_to_samples(run.headers_line.split(), lines, run.id)
    run_in.last_byte = last_byte
    crud.run.update(db, db_obj=run, obj_in=run_in)
    return samples
