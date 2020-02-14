import pytest


@pytest.fixture(scope="module")
def superuser_token_headers():
    from app.tests.utils import get_superuser_token_headers
    return get_superuser_token_headers()


@pytest.fixture(scope="module")
def normal_user_token_headers():
    from app import config
    from app.tests.utils.user import user_authentication_headers
    return user_authentication_headers(email=config.EMAIL_TEST_USER, password=config.TEST_PASSWORD)
