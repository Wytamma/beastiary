from typing import Any, List, Tuple
import math
from beastiary.models.trace import Trace
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps
from beastiary.api.core import check_for_new_samples
from beastiary.log import logger

router = APIRouter()


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
        raise HTTPException(404, detail="Trace not found!")

    samples = crud.sample.get_multi_by_trace(
        db, trace_id=trace.id, skip=skip, limit=limit
    )

    logger.debug(f"{limit} samples requested - {len(samples)} found")
    if len(samples) < limit:

        logger.debug(f"Checking for new samples in {trace.path}")
        try:
            check_for_new_samples(db, trace=trace)
        except Exception as e:
            raise HTTPException(500, detail=f"Could read samples in {trace.path}")
        # get samples
        samples = crud.sample.get_multi_by_trace(
            db, trace_id=trace.id, skip=skip, limit=limit
        )
    logger.debug(f"Returning {len(samples)} samples")
    return samples
