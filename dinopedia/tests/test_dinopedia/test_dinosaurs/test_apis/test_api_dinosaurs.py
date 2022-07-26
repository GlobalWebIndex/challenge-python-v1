import json
import pytest
from model_bakery import baker
from typing import List
from dinosaurs.models import Dinosaur
from .utils import create_

BAKERPATH = "tests.test_dinopedia.test_dinosaurs.baker_recipes"


class TestDinosaurEndpoint:

    #
    endpoint = "/api/dinosaurs"
    #
    recipe = "dinosaur_recipe"
    dino_recipe = f"{BAKERPATH}.{recipe}"

    @pytest.mark.django_db
    def test_list(self, api_client, admin):

        #
        quantity = 2
        baker.make_recipe(self.dino_recipe, _quantity=quantity)

        #
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity

    @pytest.mark.django_db
    def test_delete(self, api_client, admin):

        # make 2
        quantity = 2
        results = baker.make_recipe(self.dino_recipe, _quantity=quantity)

        # delete 1
        response = api_client.delete(f"{self.endpoint}/{results[0].id}")

        assert response.status_code == 204

        # check that we have one left
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity - 1

    @pytest.mark.django_db
    def test_create(self, api_client, admin):

        #
        period = create_("period")
        period_id = period[0].id
        #
        size = create_("size")
        size_id = size[0].id
        #
        eat = create_("eat")
        eating_type_id = eat[0].id

        #
        colours = ["red", "blue", "green"]        

        payload = {
            "name": "Dino POST",
            "description": "ad description",
            "typical_colours": colours,
            "period": period_id,
            "size": size_id,
            "eating_type": eating_type_id,
        }

        # post request
        response = api_client.post(self.endpoint, payload)
        # results
        content = json.loads(response.content)

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_patch_colours(self, api_client, admin):
        #
        quantity = 2
        dinos = create_("dinosaur", quantity)

        dino_id = dinos[0].id

        # typical colours is [black] in the recipe
        # we patch to white
        payload = {
            "typical_colours": ["white"],
        }

        # patch request
        url = f"{self.endpoint}/{dino_id}"
        response = api_client.patch(url, payload)
        # results
        content = json.loads(response.content)

        assert response.status_code == 200
        assert content["typical_colours"] == ["white"]

    @pytest.mark.django_db
    def test_integrity_error_for_dinos_with_the_same_name(self, api_client, admin):
        """
        Two dinosqurs cannot have the same name
        """
        with pytest.raises(Exception) as excinfo:
            dino1 = baker.make_recipe(
                self.dino_recipe,
                name="Dinosaur 1",
            )
            dino2 = baker.make_recipe(
                self.dino_recipe,
                name="Dinosaur 1",
            )
        assert "ExceptionInfo IntegrityError" in str(excinfo)
        # assert (
        #     'duplicate key value violates unique constraint "unique_dinosaur_name"'
        #     in excinfo.value.args[0]
        # )

    # TODO create tests for every orther conflict

    # TODO create tests for filters

