from beastiary.schemas import sample
from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Run])
def get_runs(
    uuid: str = None,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve runs.
    """
    runs = crud.run.get_multi(db=db, skip=skip, limit=limit)
    return runs


def get_headers(path):
    with open(path, "r") as f:
        headers_set = False
        while True:
            line = f.readline()
            if line.startswith("#"):
                continue
            return f.tell(), line


@router.post("/", response_model=schemas.Run)
def create_run(
    *,
    uuid: str = None,
    db: Session = Depends(deps.get_db),
    run_in: schemas.RunCreate,
) -> Any:
    """
    Create new run.
    """
    # get headers
    try:
        first_byte, headers = get_headers(run_in.path)
    except FileNotFoundError as e:
        raise HTTPException(404, e.strerror)
    headers = headers.split()
    headers[0] = "sample"
    run_in.headers_line = " ".join(headers)
    run_in.first_byte = first_byte
    run_in.last_byte = first_byte
    print(run_in)
    run = crud.run.create(db=db, obj_in=run_in)
    return run
