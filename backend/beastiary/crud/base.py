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
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(self.model.__name__, db_obj)
        return db_obj

    def update(
        self,
        db: Database,
        *,
        db_obj: InDBSchemaType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> InDBSchemaType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return db_obj

    def remove(self, db: Database, *, id: int) -> InDBSchemaType:
        obj = db.query(self.model.__name__, id=id)
        if not obj:
            raise ValueError(f"{obj} not found!")
        db.delete(obj)
        return obj
