from app import config
from app.tests.utils.general import test_client


def test_get_access_token():
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    r = test_client.post(f"{config.API_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert r.status_code == 200


def test_use_access_token(superuser_token_headers):
    r = test_client.post(f"{config.API_PREFIX}/login/test-token", headers=superuser_token_headers)
    result = r.json()
    assert "email" in result
    assert r.status_code == 200
