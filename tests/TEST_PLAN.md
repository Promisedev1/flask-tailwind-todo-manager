# Test Plan: To-Do Manager

## Product under test

The product is a Flask task API, a browser UI, and a SQLite database.

## Scope

This assignment covers API behaviour, end-to-end user workflows, test data, exploratory testing, performance measurement, defects, and reporting.

## Risks

- [product] A task operation returns success but saves incorrect or incompelte data.
  - Impact: high; Saved task data would be unreliable.
  - Likelihood: Unk.; no evidence.
- [product] A browser action appears to work but does not presist after a reload.
  - Impact: high; the user could believe a change was saved when it was lost.
  - likelihood: Unk.; we have not tested this WF yet.
- [project] One test's data changes another test's result.
  - Impact: high; a false pass could let a defect go undetected, while a false failure coudl delay dliver and waste investigation time.
  - Likelihood: pausible before isolation; the app ses a presistent SQLite database.
- [product] Response time becomes unacceptable as the task list grows.
  - Impact: undetermined; long waits could prevent useers form managing tasks promptly, but no acceptable response time or expected task-list size is specified.
  - Likelyhood: Unk. ; we have not measured response time as the list grows.

[ISTQB CTFL §5.2.1–5.2.3, pages 52–53](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)
[ISTQB Performance Testing syllabus §2.1.3, “Selecting Performance Metrics,” page 19.](https://istqb.org/wp-content/uploads/2024/11/ISTQB-CT-PT_Syllabus_v1.0_2018.pdf)

## Test conditions

- A newly created task presists with the submitted text and an incomplete status.
- Completing a task in the browser remains completed afte the page reloads.
- Measure (reasonable benchmark time) `GET` `/api/tasks` with 0, 100, and 1000 stored tasks.

  [ISTQB CTFL §1.4.1, “Test analysis,” pages 18–19.](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)
  [ISTQB Performance Testing syllabus §2.1.3, page 19,](https://istqb.org/wp-content/uploads/2024/11/ISTQB-CT-PT_Syllabus_v1.0_2018.pdf)

## Test environment and data

- Each automated test uses an isolated SQLlite database with known starting data.

## Testability dependency

- The app fixes its SQLite database URI during import. Before automated tests run, the app needs a way to select a disposable test database before SQLAlchemy initializes.
