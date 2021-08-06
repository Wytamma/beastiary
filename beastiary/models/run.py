from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

from beastiary.db.base_class import Base


class Run(Base):
    id = Column(Integer, primary_key=True)
    path = Column(String)
    headers_line = Column(String)
    last_byte = Column(Integer)
    first_byte = Column(Integer)
