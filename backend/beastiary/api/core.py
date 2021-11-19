from pathlib import Path
from typing import Tuple, Union, List
from beastiary import crud, schemas
from beastiary.models.trace import Trace
from sqlalchemy.orm.session import Session
from beastiary.schemas.sample import SampleCreate

import os, math, errno


def get_headers(path: Path) -> Tuple[int, str]:
    with open(path, "r") as f:
        headers_set = False
        while True:
            line = f.readline()
            if line.startswith("#"):
                continue
            headers_list = line.split()
            try:
                headers_list[0] = "state"
            except IndexError:
                raise ValueError(f"Could not find headers in {path}")
            headers_line = " ".join(headers_list)
            last_byte = f.tell()
            return last_byte, headers_line


def add_trace(db: Session, trace_in: schemas.TraceCreate) -> Trace:
    if not trace_in.path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), trace_in.path)
    last_byte, headers_line = get_headers(trace_in.path)
    trace = crud.trace.create(
        db=db, obj_in=trace_in, headers_line=headers_line, last_byte=last_byte
    )
    return trace


def read_lines(trace: Trace) -> Tuple[int, list]:
    if not trace.path:
        raise ValueError("Path must be set.")
    with open(trace.path, "r") as f:
        f.seek(trace.last_byte, 0)
        lines = f.readlines()
        if lines:
            last_byte = f.tell()
        else:
            last_byte = trace.last_byte
        return last_byte, lines


def lines_to_SampleCreate(headers: list, lines: list) -> List[SampleCreate]:
    samples = []
    for line in lines:
        if not line:
            # blank lines are bad...
            # you'll have to have a smart way to handel this with the byte offset
            raise ValueError("Poorly formated line.")
        data = {}
        for header, value in zip(headers, line.split()):
            value = float(value)
            if value.is_integer():
                value = int(value)
            elif math.isnan(value) or math.isinf(value):
                value = None
            data[header] = value
        sample_in = {}
        sample_in["data"] = data
        sample_in["state"] = data["state"]
        samples.append(schemas.sample.SampleCreate(**sample_in))
    return samples


def check_for_new_samples(db: Session, trace: Trace) -> None:
    last_byte, lines = read_lines(trace)
    in_samples = lines_to_SampleCreate(trace.headers_line.split(), lines)
    if in_samples:
        crud.sample.create_multi_with_trace(db, objs_in=in_samples, trace_id=trace.id)
    # update the trace byte
    crud.trace.update(db, db_obj=trace, obj_in={"last_byte": last_byte})
