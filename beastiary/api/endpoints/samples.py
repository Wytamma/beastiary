from typing import Any, List
import os
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/samples/{path}", response_model=List[schemas.Sample])
def get_samples(
    path: str = Path(
        None, title="The path of the logfile associated with the samples."
    ),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve samples.
    """
    if path is None:
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    if not os.path.isabs(path):
        raise HTTPException(status_code=401, detail="Logfile path must be absolute.")
    logfile = crud.run.get_run_by_path(db, path=path)
    items = crud.item.get_items_by_logfile(db, path=path, skip=skip, limit=limit)
    return items
