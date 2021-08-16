from pathlib import Path
from beastiary import crud, schemas


def get_headers(path: Path):
    with open(path, "r") as f:
        headers_set = False
        while True:
            line = f.readline()
            if line.startswith("#"):
                continue
            return f.tell(), line


def add_trace(db, trace_in: schemas.TraceCreate):
    last_byte, headers = get_headers(trace_in.path)
    headers = headers.split()
    headers[0] = "state"
    headers_line = " ".join(headers)
    trace = crud.trace.create(
        db=db, obj_in=trace_in, headers_line=headers_line, last_byte=last_byte
    )
    return trace
