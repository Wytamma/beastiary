from beastiary.api.core import add_tree, check_for_new_tree_samples
from beastiary.log import logger

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request, Path

from beastiary import crud, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Tree])
def get_trees(
    request: Request,
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.Tree]:
    """
    Retrieve tress.
    """
    trees = crud.tree.get_multi(db=request.app.db, skip=skip, limit=limit)
    return trees


@router.get("/{tree_id}", response_model=schemas.Tree)
def get_tree(request: Request, tree_id: int) -> dict:
    """
    Retrieve tree.
    """
    tree = crud.tree.get(db=request.app.db, id=tree_id)
    if not tree:
        raise HTTPException(404, "Tree not found!")
    return tree


@router.post("/", response_model=schemas.Tree)
def create_tree(
    request: Request,
    *,
    tree_in: schemas.TreeCreate,
) -> dict:
    """
    Create new tree.
    """
    try:
        tree = add_tree(request.app.db, tree_in)
    except FileNotFoundError as e:
        raise HTTPException(404, detail="Could not find tree file!")
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(500, detail=f"Could not add {tree_in.path}")
    return tree


@router.get("/{tree_id}/samples", response_model=List[schemas.TreeSample])
def get_samples(
    request: Request,
    tree_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve samples.
    """
    tree = crud.tree.get(db=request.app.db, id=tree_id)
    if not tree:
        raise HTTPException(404, detail="Tree not found!")

    samples = crud.tree_sample.get_multi_by_tree(
        request.app.db, tree_id=tree["id"], skip=skip, limit=limit
    )
    logger.debug(f"{limit} samples requested - {len(samples)} found")
    if len(samples) < limit:
        logger.debug(f"Checking for new samples in {tree['path']}")
        try:
            check_for_new_tree_samples(request.app.db, tree=tree)
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(500, detail=f"Could read samples in {tree['path']}")
        # get samples
        samples = crud.tree_sample.get_multi_by_tree(
            request.app.db, tree_id=tree["id"], skip=skip, limit=limit
        )
    logger.debug(f"Returning {len(samples)} samples")
    return samples
