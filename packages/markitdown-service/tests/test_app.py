import os

os.environ["MARKITDOWN_API_KEY"] = "test-secret"

from fastapi.testclient import TestClient

from markitdown_service.app import app

client = TestClient(app)


def test_health_requires_no_auth():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_convert_without_key_is_rejected():
    response = client.post("/convert", json={"uri": "https://example.com"})
    assert response.status_code == 401


def test_convert_with_wrong_key_is_rejected():
    response = client.post(
        "/convert",
        json={"uri": "https://example.com"},
        headers={"X-API-Key": "wrong"},
    )
    assert response.status_code == 401


def test_convert_rejects_file_scheme():
    response = client.post(
        "/convert",
        json={"uri": "file:///etc/passwd"},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 422


def test_convert_data_uri():
    response = client.post(
        "/convert",
        json={"uri": "data:text/plain;base64,aGVsbG8gd29ybGQ="},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 200
    assert response.json() == {"markdown": "hello world"}


def test_about_requires_no_auth():
    response = client.get("/about")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "MarkItDown Service" in response.text


def test_convert_data_uri_text_format():
    response = client.post(
        "/convert?format=text",
        json={"uri": "data:text/plain;base64,aGVsbG8gd29ybGQ="},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "hello world"


def test_convert_rejects_invalid_format():
    response = client.post(
        "/convert?format=xml",
        json={"uri": "https://example.com"},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 422


def test_convert_upload():
    response = client.post(
        "/convert/upload",
        files={"file": ("hello.txt", b"hello world", "text/plain")},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 200
    assert response.json() == {"markdown": "hello world"}


def test_convert_upload_text_format():
    response = client.post(
        "/convert/upload?format=text",
        files={"file": ("hello.txt", b"hello world", "text/plain")},
        headers={"X-API-Key": "test-secret"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "hello world"


def test_mcp_mount_requires_key():
    response = client.post(
        "/mcp",
        json={},
        headers={"Accept": "application/json, text/event-stream"},
    )
    assert response.status_code == 401
