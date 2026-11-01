# Test cases

## API-01: Create and retrieve a taskStarting state: Empty, isolated test database.

Starting state: Empty, isolated test database.
Action: POST /api/tasks with JSON {"text": "Buy milk"}, then GET /api/tasks.
Expected: POST returns 201 and a task with an ID, text "Buy milk", and completed=false. GET returns that same task.

[: ISTQB CTFL §1.4.1, “Test design,” page 19](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)

## API-02: Reject a missing task description

- Starting state: Empty, isolated test database.
- Action: POST /api/tasks with JSON {}.
- Expected: Response status is 400, and a later GET /api/tasks returns an empty list.

[ISTQB CTFL §4.2.1, “Equivalence Partitioning,” page 39](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)

## API-03: Retrieve an existing task

- Starting state: One task named "Pay bill" exists in the isolated test database.
- Action: GET /api/tasks.
- Expected: Response status is 200 and the returned list contains that task's ID, text, and completion status.
  [ISTQB CTFL syllabus §1.4.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)

## API-04: Complete an existing task

- Starting state: One incomplete task exists.
- Action: PATCH /api/tasks/<id> with {"completed":true}, then GET /api/tasks.
- Expected: PATCH returns 200 with the same ID and text, and completed=true. GET returns the updated task.

## API-05: Reopen a completed task

- Starting state: One completed task exists.
- Action: PATCH /api/tasks/<id> with {"completed":false}, then GET /api/tasks.
- Expected: PATCH returns 200 with the same ID and text, and completed=false. GET returns the updated task. 

# API-06: Delete only the selected task
- Starting state: Two distinct tasks exist.
- Action: DELETE the first task, then GET /api/tasks
- Expected: DELETE returns 204 with an empty body. GET returns 200 with only the 
second taks, unchanged.


## E2E-01: Completion survices a page reload

- Starting state: An incompete task named "Pay bill" exists.
- Action: Open the page, mark that task complete, then reload the page.
- Expected: "Pay bill" appears in the completed list after the reload, not in the pending list.

## PERF-01: Task-list response time as data grows
- Measurement scope: Local HTTP requests to a single-threaded Werkzeug server using an in-memory SQLite database. Five warmup requests precede 100 sequential measured requests per task count. Results do not establish production capacity.
- Starting state: Separate test databases containing 0, 100, and 1000 tasks.
- Action: For each database size, warm up the app, then time 100 GET /api/tasks requests.
  - Validate each measured response contains the expected task count, 
  task texts in creation order, and completed=false for every task. Perform body checks outside the timed interval. 
- Record: Median and 95th-percentile response time, errors, app version, and machine details.
- Result: Report the measurements and trend. No pass/fail limit has been agreed yet.
- Calculation: Median uses statistics.median(). The p95 uses nearest rank: sort the 100 durations and select the 95th value.
- Environment: Record UTC run timestamp, Python version,operating system, and processor architecture alongside each workload's results.
- Report: Save one JSON file per workload in pytest's temporary directory and print its path. Inlude task count, request count, raw durations in milliseconds, median, nearest-rank p95, UTC timestamp, Python version, OS, and architecture.

[ISTQB Performance Testing syllabus §2.1.3, page 19](https://istqb.org/wp-content/uploads/2024/11/ISTQB-CT-PT_Syllabus_v1.0_2018.pdf)
