from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from beastiary.db.base_class import Base


class Sample(Base):
    id = Column(Integer, primary_key=True)
    sample = Column(Integer)
    data = Column(JSON)
    run_id = Column(Integer, ForeignKey("run.id"))
    run = relationship("Run", back_populates="samples")
