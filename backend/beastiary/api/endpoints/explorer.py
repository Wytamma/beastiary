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
    files: List[File]


@router.get("/", response_model=Dir)
def list_directory(path: Optional[str] = None) -> dict:
    """
    List the folders/files in a diretory
    """
    if not path:
        path = os.path.abspath(os.getcwd())
    files = [
        {
            "name": name,
            "path": os.path.join(path, name),
            "is_dir": os.path.isdir(os.path.join(path, name)),
        }
        for name in os.listdir(path)
        if not name.startswith(".")
    ]

    sorted_files = sorted(files, key=lambda d: d["is_dir"], reverse=True)

    directory = {
        "path": path,
        "parent": str(Path(path).parent.absolute()),
        "files": sorted_files,
    }
    return directory
