from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from beastiary.crud.base import CRUDBase
from beastiary.models.sample import Sample
from beastiary.schemas.sample import SampleCreate, SampleUpdate


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    def create_with_trace(
        self, db: Session, *, obj_in: SampleCreate, trace_id: int
    ) -> Sample:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, trace_id=trace_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi_with_trace(
        self, db: Session, *, objs_in: List[SampleCreate], trace_id: int
    ) -> List[Sample]:
        objs_in_data = [jsonable_encoder(obj_in) for obj_in in objs_in]
        for obj_in in objs_in_data:
            obj_in.update({"trace_id": trace_id})
        db_objs = [self.model(**obj_in_data) for obj_in_data in objs_in_data]
        db.add_all(db_objs)
        db.commit()
        return db_objs

    def get_multi_by_trace(
        self, db: Session, *, trace_id: int, skip: int = 0, limit: int = 100
    ) -> List[Sample]:
        return (
            db.query(self.model)
            .filter(Sample.trace_id == trace_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


sample = CRUDSample(Sample)
