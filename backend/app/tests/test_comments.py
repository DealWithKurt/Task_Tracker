from fastapi.testclient import TestClient

def test_create_and_get_comment(client: TestClient, auth_headers):
    # First, create a task
    task_res = client.post("/tasks", headers=auth_headers, json={
        "title": "Task for Comment",
        "deadline": "2050-01-01"
    })
    task_id = task_res.json()["id"]

    # Create comment
    comment_res = client.post(
        f"/tasks/{task_id}/comments",
        headers=auth_headers,
        json={"text": "This is a comment"}
    )
    assert comment_res.status_code == 200
    assert comment_res.json()["text"] == "This is a comment"
    comment_id = comment_res.json()["id"]

    # Get comments
    get_res = client.get(f"/tasks/{task_id}/comments", headers=auth_headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) >= 1
    assert get_res.json()[-1]["text"] == "This is a comment"

    # Delete comment
    del_res = client.delete(f"/comments/{comment_id}", headers=auth_headers)
    assert del_res.status_code == 200
