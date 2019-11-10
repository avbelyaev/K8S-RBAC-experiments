import pytest

from backend.app import get_app


@pytest.fixture
def app():
    app = get_app()
    return app


def test_hello_flask(client):
    response = client.get("/api/hello")

    assert response.status_code == 200
    assert response.json['info'] == 'Hello flask!'


def test_should_return_empty_list_of_items(client, mocker):
    mocker.patch('backend.app.DataSource.find_all', return_value=[])
    response = client.get("/api/docs")

    assert response.status_code == 200
    assert response.json['items'] == []


def test_should_return_list_of_items(client, mocker):
    expected_items = [
        {
            'firstname': 'tony',
            'lastname': 'stark'
        },
        {
            'firstname': 'steve',
            'lastname': 'rogers'
        }
    ]
    # mock DataStore inside the scope of backend.app module
    mocker.patch('backend.app.DataSource.find_all', return_value=expected_items)
    response = client.get("/api/docs")

    assert response.status_code == 200
    assert response.json['items'] == expected_items
