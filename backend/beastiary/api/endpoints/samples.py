from typing import Any, List, Tuple
import math
from beastiary.models.trace import Trace
from beastiary.schemas.sample import SampleCreate
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from beastiary import crud, schemas
from beastiary.api import deps
from beastiary.log import logger

router = APIRouter()


def read_lines(trace: Trace) -> Tuple[int, list]:
    if not trace.path:
        raise ValueError("Path must be set.")
    with open(trace.path, "r") as f:
        f.seek(trace.last_byte, 0)
        lines = f.readlines()
        if lines:
            last_byte = f.tell()
        else:
            last_byte = trace.last_byte
        return last_byte, lines


def lines_to_SampleCreate(headers: list, lines: list) -> List[SampleCreate]:
    samples = []
    for line in lines:
        if not line:
            # blank lines are bad...
            # you'll have to have a smart way to handel this with the byte offset
            raise ValueError("Poorly formated line.")
        data = {}
        for header, value in zip(headers, line.split()):
            value = float(value)
            if value.is_integer():
                value = int(value)
            elif math.isnan(value) or math.isinf(value):
                value = None
            data[header] = value
        sample_in = {}
        sample_in["data"] = data
        sample_in["state"] = data["state"]
        samples.append(schemas.sample.SampleCreate(**sample_in))
    return samples


def check_for_new_samples(db: Session, trace: Trace) -> None:
    last_byte, lines = read_lines(trace)
    in_samples = lines_to_SampleCreate(trace.headers_line.split(), lines)
    if in_samples:
        crud.sample.create_multi_with_trace(db, objs_in=in_samples, trace_id=trace.id)
    # update the trace byte
    crud.trace.update(db, db_obj=trace, obj_in={"last_byte": last_byte})


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

    logger.debug(f"{len(samples)} found, {limit} samples requested")
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
