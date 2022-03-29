from typing import List
from beastiary.db.database import Database

from fastapi.encoders import jsonable_encoder

from beastiary.crud.base import CRUDBase
from beastiary.schemas.sample import SampleCreate, SampleUpdate, Sample


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    def create_multi(self, db: Database, *, objs_in: List[dict]) -> List[Sample]:
        db.add_all(self.model.__name__, objs_in)
        return objs_in

    def get_multi_by_trace(
        self, db: Database, *, trace_id: int, skip: int = 0, limit: int = 100
    ) -> List[Sample]:
        return db.query(self.model.__name__, skip=skip, limit=limit, trace_id=trace_id)


sample = CRUDSample(Sample)
