from model_bakery.recipe import Recipe, foreign_key, seq
from dinosaurs.models import (
    DinoOwner,
    Dinosaur,
    Period,
    EatingType,
    DinoSize,
)
from pytz import timezone


# no foreign keys - do not need specific order
period_recipe = Recipe(Period, name=seq("Period "))
size_recipe = Recipe(DinoSize)
eat_recipe = Recipe(EatingType)

# with foreign keys - need specific order
dinosaur_recipe = Recipe(
    Dinosaur,
    name=seq("Dino "),
    period=foreign_key(period_recipe),
    size=foreign_key(size_recipe),
    eating_type=foreign_key(eat_recipe),
)


