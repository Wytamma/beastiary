from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from beastiary.db.database import Database

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

InDBSchemaType = TypeVar("InDBSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[InDBSchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[InDBSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Pydantic model (schema) class for in database representation
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Database, id: Any) -> Optional[InDBSchemaType]:
        return db.query(self.model.__name__, id=id)

    def get_multi(
        self, db: Database, *, skip: int = 0, limit: int = 100
    ) -> List[InDBSchemaType]:
        return db.query(self.model.__name__, skip=skip, limit=limit)

    def create(self, db: Database, *, obj_in: CreateSchemaType) -> InDBSchemaType:
        db_obj = jsonable_encoder(obj_in)
        db.add(self.model.__name__, db_obj)
        return db_obj

    def update(
        self,
        db: Database,
        *,
        db_obj: dict,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> InDBSchemaType:
        db_obj.update(obj_in)
        return db_obj
