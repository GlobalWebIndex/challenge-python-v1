from model_bakery.recipe import Recipe, foreign_key, seq
from dinosaurs.models import (
    DinoOwner,
    Dinosaur,
    Period,
    EatingType,
    DinoSize,
    PetDinosaur,
)



# no foreign keys - do not need specific order
period_recipe = Recipe(
    Period,
    name=seq("Period "),
    start_year=2000,
    end_year=1900,
)
size_recipe = Recipe(DinoSize)
eat_recipe = Recipe(EatingType)

# with foreign keys - need specific order
dinosaur_recipe = Recipe(
    Dinosaur,
    name=seq("Dino "),
    typical_colours = ["black"],
    period=foreign_key(period_recipe),
    size=foreign_key(size_recipe),
    eating_type=foreign_key(eat_recipe),
)
petDinosaur_recipe = Recipe(
    PetDinosaur,
    dino_type = foreign_key(dinosaur_recipe),
    pet_name=seq("PetDino "),
    colour = "flashy colours",
    age = seq(1, 2),
)


