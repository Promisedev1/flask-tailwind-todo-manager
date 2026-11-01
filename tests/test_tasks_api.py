# API-01: Create and retrieve a taskStarting state: Empty, isolated test database.
def test_create_task_returns_created_task(client):
    post_response = client.post("/api/tasks", json={"text": "Buy milk"})
    assert post_response.status_code == 201

    created = post_response.get_json()
    assert isinstance(created["id"], int)
    assert created["id"] > 0
    assert created["text"] == "Buy milk"
    assert created["completed"] is False

    get_response = client.get("/api/tasks")
    assert get_response.status_code == 200
    assert get_response.get_json() == [created]

# API-02: Reject a missing task description
def test_missing_description_is_rejected(client):
    response = client.post("/api/tasks", json={})
    assert response.status_code == 400
    assert client.get("/api/tasks").get_json() == []

# API-03: Retrieve an existing task
def test_get_existing_task(client):
    created = client.post("/api/tasks", json={"text": "Pay bill"}).get_json()

    response = client.get("/api/tasks")

    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == created["id"]
    assert tasks[0]["text"] == "Pay bill"
    assert tasks[0]["completed"] is False

# API-04: Complete an existing task
def test_complete_existing_task(client):
    response = client.post("/api/tasks", json={"text": "Pay bill"})
    assert response.status_code == 201
    created = response.get_json()
    assert created["completed"] is False
    response = client.patch(
        f"/api/tasks/{created['id']}",
        json={"completed": True},
    )
    assert response.status_code == 200

    updated = response.get_json()
    assert updated["id"] == created["id"]
    assert updated["text"] == created["text"]
    assert updated["completed"] is True

    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == [updated]


# API-05: Reopen a completed task
def test_reopen_completed_task(client):
    response = client.post("/api/tasks", json={"text": "Pay bill"})
    assert response.status_code == 201
    created = response.get_json()

    response = client.patch(
        f"/api/tasks/{created['id']}",
        json={"completed": True},
    )
    assert response.status_code == 200
    assert response.get_json()["completed"] is True

    response = client.patch(
        f"/api/tasks/{created['id']}",
        json={"completed": False},
    )
    assert response.status_code == 200

    reopened = response.get_json()
    assert reopened["id"] == created["id"]
    assert reopened["text"] == created["text"]
    assert reopened["completed"] is False

    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == [reopened]

