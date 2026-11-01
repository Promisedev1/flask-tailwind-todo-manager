from playwright.sync_api import Page, expect

## E2E-01: Completion survices a page reload
def test_completion_persists_after_reload(page: Page, live_server_url, client):
    setup_response = client.post("/api/tasks", json={"text": "Pay bill"})
    assert setup_response.status_code == 201
    task_id = setup_response.get_json()["id"]

    page.goto(live_server_url)
    pending = page.locator(f"#pending-tasks-list #task-{task_id}")
    expect(pending).to_contain_text("Pay bill")

    pending.locator("button").first.click()

    completed = page.locator(f"#completed-tasks-list #task-{task_id}")
    expect(completed).to_contain_text("Pay bill")

    page.reload()
    expect(completed).to_contain_text("Pay bill")
    expect(pending).not_to_be_visible()
