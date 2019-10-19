from unittest import mock
from unittest.mock import Mock

import pytest

from backend.app import get_app_for_test


@pytest.fixture
def app():
    app = get_app_for_test()
    return app


def test_hello_flask(client):
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json['msg'] == 'Hello flask!'


@mock.patch('backend.mongo')
def test_should_return_list_of_items(client, mock):
    mock_methods = {'fuck.return_value': 3}
    mongo_mock = Mock(**mock_methods)
    print(mongo_mock.fuck())
    mocker.patch('backend.mongo', return_value=mongo_mock)
    response = client.get("/api/docs")
    assert response.json['items'] == None
