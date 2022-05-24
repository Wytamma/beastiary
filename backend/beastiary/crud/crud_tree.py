from beastiary.log import logger
from typing import List
from beastiary.db import Database

from beastiary.crud.base import CRUDBase
from beastiary.schemas.tree import TreeCreate, TreeUpdate, Tree
from beastiary.schemas.tree_sample import TreeSample, SampleCreate, SampleUpdate


class CRUDTree(CRUDBase[Tree, TreeCreate, TreeUpdate]):
    def create(  # type: ignore
        self, db: Database, *, obj_in: TreeCreate, last_byte: int, translation: dict
    ) -> Tree:
        tree = obj_in.dict()
        tree.update(
            last_byte=last_byte,
            translation=translation,
            id=len(db.data[self.model.__name__]),
        )
        logger.debug(f"Adding Tree: {tree}")
        db.add(self.model.__name__, tree)
        return tree


class CRUDSample(CRUDBase[TreeSample, SampleCreate, SampleUpdate]):
    def create_multi(self, db: Database, *, objs_in: List[dict]) -> List[TreeSample]:
        db.add_all(self.model.__name__, objs_in)
        return objs_in

    def get_multi_by_tree(
        self, db: Database, *, tree_id: int, skip: int = 0, limit: int = 100
    ) -> List[TreeSample]:
        return db.query(self.model.__name__, skip=skip, limit=limit, tree_id=tree_id)


sample = CRUDSample(TreeSample)
tree = CRUDTree(Tree)
