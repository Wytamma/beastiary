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


# from typing import TYPE_CHECKING

# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

# from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .user import User  # noqa: F401


# class Item(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("user.id"))
#     owner = relationship("User", back_populates="items")
