from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Run])
def get_runs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve runs.
    """
    runs = crud.run.get_multi(db=db, skip=skip, limit=limit)
    return runs
