from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from beastiary.crud.base import CRUDBase
from beastiary.models.sample import Sample
from beastiary.schemas.sample import SampleCreate, SampleUpdate


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    def get_multi_by_path(
        self, db: Session, *, logfile_id: int, skip: int = 0, limit: int = 100
    ) -> List[Sample]:
        return (
            db.query(self.model)
            .filter(Sample.logfile_id == logfile_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


sample = CRUDSample(Sample)
