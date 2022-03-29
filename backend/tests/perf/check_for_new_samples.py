from beastiary import crud, schemas
from beastiary.api.core import add_trace, check_for_new_samples
from beastiary.db.database import Database


db = Database()
db.create_table("Trace")
db.create_table("Sample")

path = "tests/data/beast1.log"

trace = add_trace(db, schemas.TraceCreate(path=str(path)))

check_for_new_samples(db, trace=trace)

samples = crud.sample.get_multi_by_trace(db, trace_id=trace["id"], skip=0, limit=5000)
