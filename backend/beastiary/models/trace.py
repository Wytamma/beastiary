from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from beastiary.db.base_class import Base

if TYPE_CHECKING:
    from beastiary.models.sample import Sample


class Trace(Base):
    id = Column(Integer, primary_key=True)
    path = Column(String)
    headers_line = Column(String, default="")
    last_byte = Column(Integer, default=0)
    samples = relationship("Sample", back_populates="trace")
