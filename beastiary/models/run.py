from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from beastiary.db.base_class import Base


class Run(Base):
    id = Column(Integer, primary_key=True)
    path = Column(String)
    samples = relationship("Sample", back_populates="run")
