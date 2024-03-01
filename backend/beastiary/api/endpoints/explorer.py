from typing import Any, List, Optional
import os
from pathlib import Path
from fastapi import APIRouter, Depends

router = APIRouter()


from pydantic import BaseModel


class File(BaseModel):
    name: str
    path: str
    is_dir: bool


class Dir(BaseModel):
    path: str
    parent: str
    is_root: bool
    files: List[File]


@router.get("/", response_model=Dir)
def list_directory(path: Optional[str] = None) -> dict:
    """
    List the folders/files in a diretory
    """
    cwd = os.getcwd()
    if not path:
        path = os.path.abspath(cwd)
    # check it path is cwd or child of cwd
    if path and not os.path.abspath(path).startswith(cwd):
        path = os.path.abspath(cwd)
    # make path relative to cwd
    path = os.path.relpath(path, cwd)
    print(path)
    files = [
        {
            "name": name,
            "path": os.path.join(path, name),
            "is_dir": os.path.isdir(os.path.join(path, name)),
        }
        for name in os.listdir(path)
        if not name.startswith(".")
    ]

    sorted_files = sorted(files, key=lambda d: d["name"])
    sorted_folders = sorted(sorted_files, key=lambda d: d["is_dir"], reverse=True)

    directory = {
        "path": path,
        "parent": str(Path(path).parent),
        "files": sorted_folders,
        "is_root": path == ".",
    }
    return directory
