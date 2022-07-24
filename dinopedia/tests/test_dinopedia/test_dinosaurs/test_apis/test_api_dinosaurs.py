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
    dino_recipe = f"{BAKERPATH}.{recipe}"

    @pytest.mark.django_db
    def test_list(self, api_client, admin):

        quantity = 2
        baker.make_recipe(self.dino_recipe, _quantity = quantity)
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity

    
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
        assert 'duplicate key value violates unique constraint "unique_dinosaur_name"' in excinfo.value.args[0]
    
    # TODO create tests for every orther conflict

    # TODO test to put, patch, delete

    @pytest.mark.django_db
    def test_delete(self, api_client, admin):

        # make 2
        quantity = 2
        results = baker.make_recipe(self.dino_recipe, _quantity = quantity)

        # delete 1
        response = api_client.delete(f"{self.endpoint}/{results[0].id}")

        assert response.status_code == 204
        
        # check that we have one left
        response = api_client.get(self.endpoint)
        results = json.loads(response.content)["results"]

        assert response.status_code == 200
        assert len(results) == quantity-1