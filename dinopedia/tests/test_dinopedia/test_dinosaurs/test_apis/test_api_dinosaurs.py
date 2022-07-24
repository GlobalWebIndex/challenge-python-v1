import json
import pytest
from model_bakery import baker
from dinosaurs.models import Dinosaur

BAKERPATH = "tests.test_dinopedia.test_dinosaurs.baker_recipes"
class TestDinosaurEndpoint:

    #
    endpoint = "/api/dinosaurs"
    #
    recipe = "dinosaur_recipe"
    booking_recipe = f"{BAKERPATH}.{recipe}"

    @pytest.mark.django_db
    def test_list(self, api_client, admin):

        quantity = 2
        baker.make_recipe(self.booking_recipe, _quantity = quantity)
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity

    # TODO test to do conflicts
    # TODO test to put, patch, delete