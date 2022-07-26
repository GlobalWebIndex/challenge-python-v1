import json
import pytest
from model_bakery import baker
from .utils import create_

BAKERPATH = "tests.test_dinopedia.test_dinosaurs.baker_recipes"


class TestPetDinosaurEndpoint:

    #
    endpoint = "/api/petdinosaurs"
    #
    recipe = "petDinosaur_recipe"
    petdino_recipe = f"{BAKERPATH}.{recipe}"

    @pytest.mark.django_db
    def test_list(self, api_client, admin):

        #
        quantity = 2
        baker.make_recipe(self.petdino_recipe, _quantity=quantity)

        #
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity


    @pytest.mark.django_db
    def test_delete(self, api_client, admin):

        # make 2
        quantity = 2
        results = create_("petDinosaur", quantity)

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

        # create dinosaur type
        dinosaur = create_("dinosaur")
        dinosaur_id = dinosaur[0].id

        #
        colour = "white"

        payload = {
            "dino_type": dinosaur_id,
            "pet_name": "WaterMelon2",
            "age": 1,
            "height": 0.001,
            "length": 0.001,
            "width": 0.001,
            "weight": 0.001,
            "colour": colour,
            "diet": "water",
            "pet_description": "this is a dino who drinks only water",
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
        dinos = create_("petDinosaur", quantity)

        dino_id = dinos[0].id

        # typical colours is [black] in the recipe
        # we patch to white
        payload = {
            "colour": "white",
        }

        # patch request
        url = f"{self.endpoint}/{dino_id}"
        response = api_client.patch(url, payload)
        # results
        content = json.loads(response.content)

        assert response.status_code == 200
        assert content["colour"] == "white"


    @pytest.mark.django_db
    def test_integrity_error_for_petdinos_with_the_same_name_and_colour(self, api_client, admin):
        """
        Two pet dinosaurs cannot have the same name and colour
        """
        with pytest.raises(Exception) as excinfo:
            dino1 = baker.make_recipe(
                self.petdino_recipe,
                pet_name="Dinosaur 1",
            )
            dino2 = baker.make_recipe(
                self.petdino_recipe,
                pet_name="Dinosaur 1",
            )
        assert "ExceptionInfo IntegrityError" in str(excinfo)
        # assert (
        #     'duplicate key value violates unique constraint "unique_name_colour"'
        #     in excinfo.value.args[0]
        # )

    # TODO create tests for every orther conflict

    # TODO create tests for filters order etc.