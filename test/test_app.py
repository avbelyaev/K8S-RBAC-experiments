import pytest

from app import get_app_for_test


@pytest.fixture
def app():
    app = get_app_for_test()
    return app


def test_hello_flask(client):
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json['msg'] == 'Hello flask!'

