import pytest
from run import app, db, Task
from urllib.request import urlopen
from time import perf_counter_ns
from statistics import median
import json
import platform
from math import ceil
from datetime import datetime, timezone

@pytest.mark.parametrize("task_count", [0, 100, 1000])
def test_task_list_response_time(client, live_server_url, task_count, tmp_path):
    with app.app_context():
        db.session.add_all(Task(text=f"Task {i}") for i in range(task_count))
        db.session.commit()

    run_utc = datetime.now(timezone.utc).isoformat()
    print(f"run_utc={run_utc}")

    print(
        f"Python={platform.python_version()}, "
        f"OS={platform.platform()}, architecture={platform.machine()}"
    )

    for _ in range (5):
        with urlopen(f"{live_server_url}/api/tasks", timeout=10) as response: 
            assert response.status == 200
            response.read()
    
    durations_ms = []
    for _ in range(100):
        start = perf_counter_ns()
        with urlopen(f"{live_server_url}/api/tasks", timeout=10) as response:
            assert response.status == 200
            body = response.read()
        durations_ms.append((perf_counter_ns() - start) /1_000_000)
        tasks = json.loads(body)
        assert isinstance(tasks, list)
        assert len(tasks) == task_count
        assert [task["text"] for task in tasks] == [
            f"Task {i}" for i in range(task_count)
        ]
        assert all(task["completed"] is False for task in tasks)
    
    assert len(durations_ms) == 100
    median_ms = median(durations_ms)
    ordered_ms = sorted(durations_ms)
    p95_ms = ordered_ms[ceil(0.95 * len(ordered_ms)) - 1]
    print(f"tasks={task_count}, requests={len(durations_ms)}, "
        f"p95={p95_ms:.3f} ms, median={median_ms:.3f} ms"
    )

    report_path = tmp_path / "performance.json"
    report_path.write_text(
        json.dumps({
            "task_count": task_count,
            "requests": len(durations_ms),
            "median_ms": median_ms,
            "p95_ms": p95_ms,
            "durations_ms": durations_ms,
            "run_utc": run_utc,
            "python_version": platform.python_version(),
            "os": platform.platform(),
            "architecture": platform.machine(),
            "warmup_requests": 5,
            "concurrent_requests": 1,
            "p95_method": "nearest_rank",
            "measurement_scope": "local_http_in_memory_sqlite",
        }, indent=2),
        encoding="utf-8",
    )
    print(f"report={report_path}")
        


