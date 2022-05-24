from beastiary.log import logger
from typing import List
from beastiary.db import Database

from beastiary.crud.base import CRUDBase
from beastiary.schemas.trace import TraceCreate, TraceUpdate, Trace
from beastiary.schemas.trace_sample import SampleCreate, SampleUpdate, TraceSample


class CRUDTrace(CRUDBase[Trace, TraceCreate, TraceUpdate]):
    def create(  # type: ignore
        self, db: Database, *, obj_in: TraceCreate, headers_line: str, last_byte: int
    ) -> Trace:
        trace = obj_in.dict()
        trace.update(
            last_byte=last_byte,
            headers_line=headers_line,
            id=len(db.data[self.model.__name__]),
        )
        logger.debug(f"Adding Trace: {trace}")
        db.add(self.model.__name__, trace)
        return trace


class CRUDSample(CRUDBase[TraceSample, SampleCreate, SampleUpdate]):
    def create_multi(self, db: Database, *, objs_in: List[dict]) -> List[TraceSample]:
        db.add_all(self.model.__name__, objs_in)
        return objs_in

    def get_multi_by_trace(
        self, db: Database, *, trace_id: int, skip: int = 0, limit: int = 100
    ) -> List[TraceSample]:
        return db.query(self.model.__name__, skip=skip, limit=limit, trace_id=trace_id)


trace = CRUDTrace(Trace)
sample = CRUDSample(TraceSample)
