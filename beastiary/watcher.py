from dataclasses import dataclass, field
from os import error
from types import coroutine
import asyncio

from beastiary.schemas import Sample
from beastiary import crud


@dataclass
class LogFile:
    path: str
    task: coroutine = None
    # hash: str


@dataclass
class Watcher:
    pool: list = field(default_factory=list)

    def watch(self, log_file_path):
        # some checks
        # check if it;s allready running
        logfile = self.get(log_file_path)
        if logfile:
            if not logfile.task.done():
                raise ValueError(
                    f"The logfile {logfile.task} if already being watched."
                )
            # remove the old logfile from loop
            self.pool = list(filter(lambda lf: lf.path != logfile.path, self.pool))
        else:
            log_file = LogFile(path=log_file_path)
        loop = asyncio.get_running_loop()
        task = loop.create_task(self.check_for_changes(log_file))
        log_file.task = task
        self.pool.append(log_file)
        return task

    async def check_for_changes(self, log_file):
        with open(log_file.path, "r") as f:
            headers_set = False
            while True:
                line = f.readline()
                if line.startswith("#"):
                    continue
                elif not headers_set:
                    headers = line
                    headers_set = True
                    line = f.readline()
                if not line:
                    await asyncio.sleep(1)
                    continue
                data = {
                    key: float(sample)
                    for key, sample in zip(headers.split(), line.split())
                }

    def stop(self):
        for task in self.tasks:
            task.cancel()

    def get(self, path):
        try:
            return next(filter(lambda logfile: logfile.path == path, self.pool)).task
        except:
            return None

    @property
    def tasks(self):
        return [logfile for logfile in self.pool if not logfile.task.done()]
