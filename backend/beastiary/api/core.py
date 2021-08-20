from pathlib import Path
from typing import Tuple, Union
from beastiary import crud, schemas
from beastiary.models.trace import Trace
from sqlalchemy.orm.session import Session
import errno
import os


def get_headers(path: Path) -> Tuple[int, str]:
    with open(path, "r") as f:
        headers_set = False
        while True:
            line = f.readline()
            if line.startswith("#"):
                continue
            return f.tell(), line


def add_trace(db: Session, trace_in: schemas.TraceCreate) -> Trace:
    if not trace_in.path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), trace_in.path)
    last_byte, headers = get_headers(trace_in.path)
    headers_list = headers.split()
    headers_list[0] = "state"
    headers_line = " ".join(headers_list)
    trace = crud.trace.create(
        db=db, obj_in=trace_in, headers_line=headers_line, last_byte=last_byte
    )
    return trace
