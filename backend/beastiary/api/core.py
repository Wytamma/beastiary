from logging import log
from pathlib import Path
from typing import Optional, Tuple, Union, List
from beastiary import crud, schemas
from beastiary.db.database import Database
from pydantic.utils import is_valid_field
from beastiary.log import logger
import os, math, errno


def get_headers(path: Path, delimiter: Optional[str] = "\t") -> Tuple[int, str]:
    logger.debug(f"Getting headers from {path}")
    with open(path, "r") as f:
        while True:
            line = f.readline()
            if line.startswith("#") or line.startswith("["):
                continue
            headers_list = line.strip().split(delimiter)
            try:
                headers_list[0] = "state"
            except IndexError:
                raise ValueError(f"Could not find headers in {path}")
            headers_line = delimiter.join(headers_list)
            last_byte = f.tell()
            logger.debug(f"last_byte = {last_byte}")
            logger.debug(f"headers_line = {headers_line}")
            logger.debug(f"delimiter = {delimiter}")
            return last_byte, headers_line


def is_valid_log_file(headers_line: str, delimiter: Optional[str] = None) -> bool:
    if len(headers_line.split(delimiter)) > 1:
        return True
    return False


def add_trace(db: dict, trace_in: schemas.TraceCreate) -> dict:
    if not trace_in.path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), trace_in.path)
    last_byte, headers_line = get_headers(trace_in.path, delimiter=trace_in.delimiter)
    if not is_valid_log_file(headers_line, delimiter=trace_in.delimiter):
        raise ValueError(f"Invalid log file: {trace_in.path}")
    logger.debug(f"Creating trace: {trace_in}")
    trace = crud.trace.create(
        db, obj_in=trace_in, last_byte=last_byte, headers_line=headers_line
    )
    logger.debug(f"Created trace: {trace}")
    return trace


def read_lines(trace: schemas.Trace) -> Tuple[int, list]:
    logger.debug(f"reading lines from: {trace}")
    if not trace["path"]:
        raise ValueError("Path must be set.")
    with open(trace["path"], "r") as f:
        f.seek(trace["last_byte"], 0)
        lines = f.readlines()
        if lines:
            last_byte = f.tell()
        else:
            last_byte = trace["last_byte"]
        logger.debug(f"last_byte = {last_byte}")
        logger.debug(f"lines found = {len(lines)}")
        return last_byte, lines


def lines_to_SampleCreate(
    headers: list, lines: list, trace_id: int, delimiter: Optional[str] = None
) -> List[dict]:
    samples = []
    for line in lines:
        data = {}
        line = line.strip()  # strip \n
        for header, value in zip(headers, line.split(delimiter)):
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
                elif math.isnan(value) or math.isinf(value):
                    value = None
            except ValueError:
                # value is not a number
                # treat as categorical
                logger.debug(f"Value is not a number: {value}")
            data[header] = value
        sample_in = {}
        sample_in["data"] = data
        sample_in["state"] = data["state"]
        sample_in["trace_id"] = trace_id
        samples.append(sample_in)
    return samples


def check_for_new_samples(db: Database, trace: schemas.Trace) -> None:
    last_byte, lines = read_lines(trace)
    in_samples = lines_to_SampleCreate(
        trace["headers_line"].split(trace["delimiter"]),
        lines,
        trace_id=trace["id"],
        delimiter=trace["delimiter"],
    )
    if in_samples:
        crud.sample.create_multi(db, objs_in=in_samples)
    # update the trace byte
    crud.trace.update(db, db_obj=trace, obj_in={"last_byte": last_byte})
