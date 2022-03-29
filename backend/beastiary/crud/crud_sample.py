from typing import List
from beastiary.db.database import Database

from fastapi.encoders import jsonable_encoder

from beastiary.crud.base import CRUDBase
from beastiary.schemas.sample import SampleCreate, SampleUpdate, Sample


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    def create_with_trace(
        self, db: Database, *, obj_in: SampleCreate, trace_id: int
    ) -> Sample:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, trace_id=trace_id)
        db.add(self.model.__name__, db_obj)
        return db_obj

    def create_multi_with_trace(
        self, db: Database, *, objs_in: List[SampleCreate], trace_id: int
    ) -> List[Sample]:
        objs_in_data = [obj_in.dict() for obj_in in objs_in]
        for obj_in in objs_in_data:
            obj_in.update({"trace_id": trace_id})
        db_objs = [self.model(**obj_in_data) for obj_in_data in objs_in_data]
        db.add_all(self.model.__name__, db_objs)
        return db_objs

    def get_multi_by_trace(
        self, db: Database, *, trace_id: int, skip: int = 0, limit: int = 100
    ) -> List[Sample]:
        return db.query(self.model.__name__, skip=skip, limit=limit, trace_id=trace_id)


sample = CRUDSample(Sample)
