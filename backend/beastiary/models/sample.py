from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship

from beastiary.db.base_class import Base

if TYPE_CHECKING:
    from beastiary.models.trace import Trace


class Sample(Base):
    id = Column(Integer, primary_key=True)
    state = Column(Integer)
    data = Column(JSON)
    trace_id = Column(Integer, ForeignKey("trace.id"))
    trace = relationship("Trace", back_populates="samples")
