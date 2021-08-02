from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Sample])
def get_samples(
    run_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve samples.
    """
    samples = crud.sample.get_multi_by_run(db=db, run_id=run_id, skip=skip, limit=limit)
    return samples
