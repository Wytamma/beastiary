from logging import log
from pathlib import Path
from typing import Tuple
from beastiary import crud, schemas
from beastiary.db.database import Database
from beastiary.log import logger
import os, errno


class NexusFile:
    path: Path = None

    def __init__(self, path) -> None:
        if not path.is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        self.path = path

    @property
    def translation(self):
        logger.debug(f"Getting translate from {self.path}")
        translation = {}
        block = False
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Translate"):
                    # start block
                    block = True
                    continue
                elif not line.startswith("Translate") and not block:
                    # outside block
                    continue
                elif line.startswith("End") or line.startswith(";") and block:
                    # end of block
                    break
                k, v = line.strip().split()
                translation[k] = v
        return translation

    @property
    def trees_starting_byte(self):
        logger.debug(f"Getting last byte from {self.path}")
        with open(self.path, "r") as f:
            last_byte = None
            current_byte = None
            while True:
                line = f.readline()
                if not line:
                    # end of file
                    break
                if line.startswith("tree "):
                    # first tree
                    last_byte = current_byte
                    break
                current_byte = f.tell()
            if not last_byte:
                raise ValueError(f"Could not find trees in {self.path}")
            logger.debug(f"last_byte = {last_byte}")
            return last_byte


def add_tree(db: dict, tree_in: schemas.TreeCreate) -> dict:
    nexus_file = NexusFile(tree_in.path)
    translation = nexus_file.translation
    last_byte = nexus_file.trees_starting_byte
    logger.debug(f"Creating tree: {tree_in}")
    tree = crud.tree.create(
        db,
        obj_in=tree_in,
        last_byte=last_byte,
        translation=translation,
    )
    logger.debug(f"Created tree: {tree}")
    return tree


def read_lines_starting_at_last_byte(tree: schemas.Tree) -> Tuple[int, list]:
    logger.debug(f"reading lines from: {tree['path']}")
    if not tree["path"]:
        raise ValueError("Path must be set.")
    lines = []
    last_byte = tree["last_byte"]
    with open(tree["path"], "r") as f:
        f.seek(tree["last_byte"], 0)
        while True:
            line = f.readline().strip()
            if not line or line.startswith("End"):
                break
            lines.append(line)
            line = f.readline().strip()
            last_byte = f.tell()
    logger.debug(f"last_byte = {last_byte}")
    logger.debug(f"lines found = {len(lines)}")
    return last_byte, lines


def format_tree_lines(lines: list, tree_id: int):
    """
    convert list of lines in the format
    tree STATE_0 = ((((((((((((((((((((((1[&type="NewZealand"]:0.03291636239703033)120[&type="Hon...
    to a list of dicts in the format
    {"tree_id": tree_id, "state": 0, "newick": "((((((((((((((((((((((1[&type="NewZealand"]:0.03291636239703033)120[&type="Hon..."}
    """
    samples = []
    for line in lines:
        tree_state, newick = line.split(" = ")
        # tree STATE_0
        state = tree_state.split("_")[-1]
        samples.append(
            {"state": int(state.strip()), "newick": newick.strip(), "tree_id": tree_id}
        )
    return samples


def check_for_new_tree_samples(db: Database, tree: schemas.Tree) -> None:
    # I'm making a trade off with speed and memory. For the log files it's
    # okay to go with speed because the files aren't big. But the Tree files
    # can easily be 1GB so I might have to index the file i.e. create a
    # state:byte map so that trees are stored on disk but read when required.

    last_byte, lines = read_lines_starting_at_last_byte(tree)
    in_samples = format_tree_lines(lines, tree_id=tree["id"])
    if in_samples:
        crud.tree_sample.create_multi(db, objs_in=in_samples)
    # update the tree byte
    crud.tree.update(db, db_obj=tree, obj_in={"last_byte": last_byte})
