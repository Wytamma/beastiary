from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Path, Request

from beastiary import crud
from beastiary.api.core import check_for_new_samples
from beastiary.log import logger

router = APIRouter()


@router.get("/")
def get_samples(
    request: Request,
    trace_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve samples.
    """
    trace = crud.trace.get(request.app.db, trace_id)
    if not trace:
        raise HTTPException(404, detail="Trace not found!")

    samples = crud.sample.get_multi_by_trace(
        request.app.db, trace_id=trace["id"], skip=skip, limit=limit
    )
    logger.debug(f"{limit} samples requested - {len(samples)} found")
    if len(samples) < limit:
        logger.debug(f"Checking for new samples in {trace['path']}")
        try:
            check_for_new_samples(request.app.db, trace=trace)
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(500, detail=f"Could read samples in {trace['path']}")
        # get samples
        samples = crud.sample.get_multi_by_trace(
            request.app.db, trace_id=trace["id"], skip=skip, limit=limit
        )
    logger.debug(f"Returning {len(samples)} samples")
    return samples
