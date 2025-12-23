def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    email = "newuser@example.com"
    activity = "Chess Club"

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert f"Signed up {email} for {activity}" in resp.json().get("message", "")

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_unregister_success(client):
    # 'michael@mergington.edu' is initially signed up for Chess Club
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Ensure present
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister
    resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp2.status_code == 200
    assert f"Unregistered {email} from {activity}" in resp2.json().get("message", "")

    # Ensure removed
    resp3 = client.get("/activities")
    assert email not in resp3.json()[activity]["participants"]


def test_unregister_not_signed_up(client):
    email = "not-signed@example.com"
    activity = "Chess Club"

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 400


def test_activity_not_found(client):
    resp = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert resp.status_code == 404

    resp2 = client.post("/activities/NonExistent/unregister?email=test@example.com")
    assert resp2.status_code == 404
