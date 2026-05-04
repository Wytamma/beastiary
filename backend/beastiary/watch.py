import fnmatch
import glob
import threading
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import List, Set

import typer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from beastiary import schemas
from beastiary.api.core import add_trace, check_for_new_samples
from beastiary.db import Database


@dataclass(frozen=True)
class WatchTarget:
    root: Path
    pattern: str
    recursive: bool


def _has_glob_magic(path: Path) -> bool:
    return any(glob.has_magic(part) for part in path.parts)


def _parse_watch_target(spec: Path) -> WatchTarget:
    expanded_spec = Path(spec).expanduser()
    if not _has_glob_magic(expanded_spec):
        if expanded_spec.exists() and expanded_spec.is_dir():
            return WatchTarget(root=expanded_spec.resolve(), pattern="*", recursive=False)
        return WatchTarget(
            root=expanded_spec.parent.resolve(),
            pattern=expanded_spec.name,
            recursive=False,
        )

    parts = expanded_spec.parts
    first_magic_index = next(
        index for index, part in enumerate(parts) if glob.has_magic(part)
    )
    root_parts = parts[:first_magic_index]
    pattern_parts = parts[first_magic_index:]
    root = Path(*root_parts) if root_parts else Path(".")
    pattern = PurePosixPath(*pattern_parts).as_posix()
    return WatchTarget(
        root=root.expanduser().resolve(),
        pattern=pattern,
        recursive="**" in pattern_parts,
    )


def _trace_exists(db: Database, path: Path) -> bool:
    return bool(db.query("Trace", path=path))


def add_startup_files(db: Database, paths: List[Path], delimiter: str) -> None:
    typer.echo("Adding log files:")
    for path in paths:
        try:
            add_trace_from_path(db, path, delimiter)
        except ValueError as e:
            typer.echo(f"❌ - {path}: {e}")
        except FileNotFoundError as e:
            typer.echo(f"❌ - {path}: {e.strerror}")
    typer.echo("")


def add_trace_from_path(db: Database, path: Path, delimiter: str) -> bool:
    resolved_path = path.expanduser().resolve()
    if _trace_exists(db, resolved_path):
        return False
    trace = add_trace(
        db,
        schemas.TraceCreate(path=resolved_path, delimiter=delimiter),
    )
    check_for_new_samples(db, trace=trace)
    typer.echo(f"✅ - {trace['path']}")
    return True


class TraceWatchHandler(FileSystemEventHandler):
    def __init__(self, db: Database, delimiter: str, targets: List[WatchTarget]) -> None:
        self.db = db
        self.delimiter = delimiter
        self.targets = targets
        self.lock = threading.Lock()
        self.reported_waiting: Set[Path] = set()

    def on_created(self, event: FileSystemEvent) -> None:
        self._handle_event(event)

    def on_modified(self, event: FileSystemEvent) -> None:
        self._handle_event(event)

    def on_moved(self, event: FileSystemEvent) -> None:
        self._handle_event(event)

    def _handle_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        candidate = Path(getattr(event, "dest_path", event.src_path)).resolve()
        if not self._matches_any_target(candidate):
            return
        with self.lock:
            try:
                added = add_trace_from_path(self.db, candidate, self.delimiter)
                if added and candidate in self.reported_waiting:
                    self.reported_waiting.remove(candidate)
            except (FileNotFoundError, ValueError):
                # Files can be discovered before headers are fully written
                if candidate not in self.reported_waiting:
                    typer.echo(f"⏳ - waiting for readable log file: {candidate}")
                    self.reported_waiting.add(candidate)

    def _matches_any_target(self, candidate: Path) -> bool:
        for target in self.targets:
            try:
                relative = candidate.relative_to(target.root)
            except ValueError:
                continue
            relative_posix = relative.as_posix()
            if not target.recursive and "/" in relative_posix:
                continue
            if fnmatch.fnmatch(relative_posix, target.pattern):
                return True
        return False


def start_watch_observer(
    db: Database,
    watch_specs: List[Path],
    delimiter: str,
) -> Observer:
    targets = [_parse_watch_target(spec) for spec in watch_specs]
    missing_roots = [target.root for target in targets if not target.root.is_dir()]
    if missing_roots:
        missing_root_list = ", ".join(str(path) for path in missing_roots)
        raise typer.BadParameter(
            f"Watch path root must exist and be a directory: {missing_root_list}"
        )

    observer = Observer()
    for root in sorted({target.root for target in targets}):
        root_targets = [target for target in targets if target.root == root]
        observer.schedule(
            TraceWatchHandler(db, delimiter, root_targets),
            str(root),
            recursive=any(target.recursive for target in root_targets),
        )
    observer.start()
    return observer
