import requests
import pytest


@pytest.mark.parametrize(
    'status_url,status_response',
    [
        (401,401),
        (200, 200),
        ('dsf', 500),
        (199, 500),
    ]
)
def test_get_request(status_url,status_response, config):
    response = requests.get(f'http://{config.get("HOST")}:{config.get("PORT")}/?status={status_url}')
    assert response.status_code == status_response
    assert 'GET' in response.text


@pytest.mark.parametrize(
    'status_url,status_response,content_type',
    [
        (401,401,'text/html'),
        (200, 200,'text/xml'),
        ('dsf', 500,'application/json'),
        (199, 500,'image/png'),
    ]
)
def test_post_request(status_url,status_response,content_type,config):
    headers = {'Content-Type': content_type}
    response = requests.post(f'http://{config.get("HOST")}:{config.get("PORT")}/?status={status_url}', headers=headers)
    assert response.status_code == status_response
    assert content_type in response.text
