from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from beastiary.crud.base import CRUDBase
from beastiary.models.trace import Trace
from beastiary.schemas.trace import TraceCreate, TraceUpdate


class CRUDTrace(CRUDBase[Trace, TraceCreate, TraceUpdate]):
    def create(  # type: ignore
        self, db: Session, *, obj_in: TraceCreate, headers_line: str, last_byte: int
    ) -> Trace:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data, headers_line=headers_line, last_byte=last_byte
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


trace = CRUDTrace(Trace)
