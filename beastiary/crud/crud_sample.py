from typing import List

from sqlalchemy.orm import Session

from beastiary.crud.base import CRUDBase
from beastiary.models.sample import Sample
from beastiary.schemas.sample import SampleCreate, SampleUpdate


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    def get_multi_by_run(
        self, db: Session, *, run_id: int, skip: int = 0, limit: int = 100
    ) -> List[Sample]:
        return (
            db.query(self.model)
            .filter(Sample.run_id == run_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


sample = CRUDSample(Sample)
