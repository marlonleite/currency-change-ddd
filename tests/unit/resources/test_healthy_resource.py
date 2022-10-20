def test_healthy_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Ok"}
