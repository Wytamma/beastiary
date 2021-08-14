from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from beastiary.db.base_class import Base


class Trace(Base):
    id = Column(Integer, primary_key=True)
    path = Column(String)
    headers_line = Column(String)
    last_byte = Column(Integer)
    samples = relationship("Sample", back_populates="trace")
