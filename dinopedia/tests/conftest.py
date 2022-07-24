# conftest.py
# Fixtures for API tests
# To create the tests you need to login to a db
# follow this: https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
# You could create also mockups -> see bakery
# https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4
#

import os
from enum import Enum

import pytest
from rest_framework.test import APIClient
# from dinopedia.dinosaurs.models import User
from django.contrib.auth.models import User


@pytest.fixture
@pytest.mark.django_db
def admin() -> User:
    username = "admin"
    password = "admin"
    user = User.objects.create_user(username=username, password=password)
    return user


@pytest.fixture
@pytest.mark.django_db
def api_client(admin) -> APIClient:
    """Create authenticated api client

    Returns:
        APIClient: with admin/superuser role
    """
    client = APIClient()
    username = "admin"
    password = "admin"
    client.login(username=username, password=password)
    return client

# @pytest.fixture()
# def baker_dest():
#     return "tests.test_s4r_api.baker_recipes."

# class S4rRecipes(Enum):
#     """The location of the recipes"""

#     BAKERPATH = os.path.split(os.path.dirname(__file__))[1]
#     POSITION_RCP = f"{BAKERPATH}.position_rcp"
#     TRAIN_RCP = f"{BAKERPATH}.train_rcp"
#     VELOCITYSENSOR_RCP = f"{BAKERPATH}.velocitySensor_rcp"
