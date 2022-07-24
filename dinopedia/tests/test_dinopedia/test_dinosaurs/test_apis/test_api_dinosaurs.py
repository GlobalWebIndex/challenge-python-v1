import json
import pytest
from model_bakery import baker
from dinosaurs.models import Dinosaur


class TestDinosaurEndpoint:

    # url is set to block but the name to blocks
    endpoint = "/api/dinosaurs"

    @pytest.mark.django_db
    def test_list(self, api_client, admin):

        quantity = 1
        baker.make(Dinosaur, _quantity = quantity)
        response = api_client.get(self.endpoint)
        data = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(data) == quantity