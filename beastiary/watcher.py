from dataclasses import dataclass, field
from types import coroutine
import asyncio


@dataclass
class LogFile:
    path: str
    task: coroutine = None
    # hash: str

@dataclass
class Watcher:
    pool: list = field(default_factory=list)
    all_tasks: list = field(default_factory=list)

    def watch(self, log_file_path):
        # some checks
        log_file = LogFile(path=log_file_path)
        loop = asyncio.get_running_loop()
        task = loop.create_task(self.check_for_changes(log_file))
        log_file.task = task
        self.pool.append(log_file)
        self.all_tasks.append(task)
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
                with open("out.txt", "a") as outfile:
                    outfile.write(log_file.path + str(data) + "\n")

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
