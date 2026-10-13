"""Simple in-process job queue so the GUI never blocks on generation."""
from __future__ import annotations

import queue
import threading
from dataclasses import dataclass
from typing import Callable


@dataclass
class Job:
    job_id: str
    payload: dict
    on_done: Callable[[object], None] | None = None


class JobQueue:
    def __init__(self, worker: Callable[[Job], object], workers: int = 1) -> None:
        self._q: queue.Queue[Job | None] = queue.Queue()
        self._worker = worker
        for _ in range(workers):
            threading.Thread(target=self._loop, daemon=True).start()

    def submit(self, job: Job) -> None:
        self._q.put(job)

    def _loop(self) -> None:
        while True:
            job = self._q.get()
            if job is None:
                return
            try:
                result = self._worker(job)
                if job.on_done:
                    job.on_done(result)
            finally:
                self._q.task_done()