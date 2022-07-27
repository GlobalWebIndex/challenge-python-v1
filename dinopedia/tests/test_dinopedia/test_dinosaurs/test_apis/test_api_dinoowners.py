import json
import pytest
from model_bakery import baker
from .utils import create_

BAKERPATH = "tests.test_dinopedia.test_dinosaurs.baker_recipes"


class TestDinoOwnersEndpoint:

    #
    endpoint = "/api/dinoowners"
    #
    recipe = "dinoOwner_recipe"
    dinoOwner_recipe = f"{BAKERPATH}.{recipe}"

    @pytest.mark.django_db
    def test_list(self, api_client, admin):

        #
        quantity = 2
        baker.make_recipe(self.dinoOwner_recipe, _quantity=quantity)

        #
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity

    @pytest.mark.django_db
    def test_delete(self, api_client, admin):

        # make 2
        quantity = 2
        results = create_("dinoOwner", quantity)

        # delete 1
        response = api_client.delete(f"{self.endpoint}/{results[0].id}")

        assert response.status_code == 204

        # check that we have one left
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity - 1

    @pytest.mark.django_db
    def test_create_with_no_pet_dino_nor_liked(self, api_client, admin):

        # post owner with no likes or pet dino :(
        payload = {
            "nickname": "Ash Ketchum2",
            "petDino": None,
            "liked_dinosaurs": []
        }

        # post request
        response = api_client.post(self.endpoint, payload)
        # results
        content = json.loads(response.content)

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_create(self, api_client, admin):

        # create dinosaur type
        dinosaur = create_("dinosaur")
        dinosaur_id = dinosaur[0].id

        # create pet dino
        petDinosaur = create_("petDinosaur")
        petDinosaur_id = petDinosaur[0].id

        # post owner
        payload = {
            "nickname": "Ash Ketchum2",
            "petDino": petDinosaur_id,
            "liked_dinosaurs": [dinosaur_id]
        }

        # post request
        response = api_client.post(self.endpoint, payload)
        # results
        content = json.loads(response.content)

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_patch_nickname(self, api_client, admin):
        #
        quantity = 2
        dinos = create_("dinoOwner", quantity)

        dino_id = dinos[0].id

        # typical colours is [black] in the recipe
        # we patch to white
        payload = {
            "nickname": "Red Ketchum",
        }

        # patch request
        url = f"{self.endpoint}/{dino_id}"
        response = api_client.patch(url, payload)
        # results
        content = json.loads(response.content)

        assert response.status_code == 200
        assert content["nickname"] == "Red Ketchum"


    @pytest.mark.django_db
    def test_integrity_error_for_petdinos_with_the_same_name_and_colour(self, api_client, admin):
        """
        Two pet dinosaurs cannot have the same name and colour
        """
        with pytest.raises(Exception) as excinfo:
            dino1 = baker.make_recipe(
                self.dinoOwner_recipe,
                nickname="Ash Ketchum",
            )
            dino2 = baker.make_recipe(
                self.dinoOwner_recipe,
                nickname="Ash Ketchum",
            )
        assert "ExceptionInfo IntegrityError" in str(excinfo)
        # assert (
        #     'duplicate key value violates unique constraint "unique_name_colour"'
        #     in excinfo.value.args[0]
        # )

    # TODO create tests for every orther conflict

    # TODO create tests for filters order etc.