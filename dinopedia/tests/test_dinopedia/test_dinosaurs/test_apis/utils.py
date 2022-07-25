from typing import List
from model_bakery import baker

BAKERPATH = "tests.test_dinopedia.test_dinosaurs.baker_recipes"

def create_(arg_: str, quantity: int =1)-> List:
    """utility function to create a model and return a list of objects

    Args:
        arg_ (_type_): the model to create
        quantity (int, optional): amount of models. Defaults to 1.

    Returns: list of the created models
    """
    recipe = f"{BAKERPATH}.{arg_}_recipe"
    creation = baker.make_recipe(recipe, _quantity=quantity)
    return creation