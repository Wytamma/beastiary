from dataclasses import dataclass


@dataclass
class LogFile:
    path: str
    hash: str


class Watcher:
    pool = []

    def __init__(self):
        # check db for log files
        pass

    def watch(self, log_file):
        # some checks
        self.pool.append(log_file)

    def check_for_changes(self, log_file):
        pass

    def run(self):

        for logfile in pool:
            with open(log_file_path, "r") as f:
                while True:
                    headers_set = False
                    line = f.readline()
                    if line.startswith("#"):
                        continue
                    elif not headers_set:
                        headers = f.readline()
                        headers_set = True
                    if not line:
                        time.sleep(0.1)
                        continue
                    data = {
                        key: float(sample) for key, sample in zip(headers, line.split())
                    }
                    print(data)
                    sample = Sample(
                        run_id=run.id, sample_id=int(data["Sample"]), data=data
                    )
                    session.add(sample)
                    session.commit()
