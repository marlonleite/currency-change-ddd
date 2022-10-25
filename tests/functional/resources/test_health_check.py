def test_health_check_endpoint(client):
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message": "Ok"}
