from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class Period(models.Model):
    """Years are in BC, so the start year is always greater than the end year
    Names : triassic , jurassic, cretaceous, paleogene, neogene
    deliberately not in a choices field in case we want to add something new!!!
    """

    name = models.CharField(null=False, max_length=15)
    start_year = models.IntegerField(null=False)
    end_year = models.IntegerField(null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} : from {self.start_year} to {self.end_year} BC"

    class Meta:
        ordering = ["name", "start_year"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_period_name"),
            models.CheckConstraint(
                check=Q(
                    end_year__lte=F("start_year"),
                ),
                name="end_after_start",
            ),
        ]


class DinoSize(models.Model):
    """
    which is a bigger dinosaur, the tall or the heavy?

    tiny, very small, small, medium, large, very large
    - length (m) - min -> max
    - height (m) - min -> max
    - width (m) - min -> max
    - weight (kgs) - min -> max
    """

    class SizeCategory(models.TextChoices):
        TINY = "TN", _("Tiny")
        VERY_SMALL = "VS", _("Very small")
        SMALL = "S", _("Small")
        MEDIUM = "M", _("Medium")
        LARGE = "L", _("Large")
        VERY_LARGE = "VL", _("Very large")
        GIGANTIC = "G", _("Gigantic")

    size = models.CharField(
        max_length=15,
        choices=SizeCategory.choices,
        null=False,
        blank=False,
    )

    #
    height_min = models.FloatField(
        default=1.0, null=False, blank=False, validators=[MinValueValidator(0.001)]
    )
    height_max = models.FloatField(
        default=100.0, null=False, blank=False, validators=[MinValueValidator(0.001)]
    )

    #
    length_min = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )
    length_max = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )

    #
    width_min = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )
    width_max = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )

    #
    weight_min = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )
    weight_max = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )

    def __str__(self):
        return f"{self.size} : from {self.height_min} to {self.height_max} meters"

    class Meta:
        ordering = ["height_min"]
        constraints = [
            models.UniqueConstraint(fields=["size"], name="unique_dino_size"),
            models.CheckConstraint(
                check=Q(
                    length_max__gt=F("length_min"),
                ),
                name="max_length_gt_min",
            ),
            models.CheckConstraint(
                check=models.Q(length_max__gte=0), name="lenght_max_positive"
            ),
            models.CheckConstraint(
                check=models.Q(length_min__gte=0), name="lenght_min_positive"
            ),
            models.CheckConstraint(
                check=Q(
                    height_max__gt=F("height_min"),
                ),
                name="max_height_gt_min",
            ),
            models.CheckConstraint(
                check=models.Q(height_max__gte=0), name="height_max_positive"
            ),
            models.CheckConstraint(
                check=models.Q(height_min__gte=0), name="height_min_positive"
            ),
            models.CheckConstraint(
                check=Q(
                    width_max__gt=F("width_min"),
                ),
                name="max_width_gt_min",
            ),
            models.CheckConstraint(
                check=models.Q(width_max__gte=0), name="width_max_positive"
            ),
            models.CheckConstraint(
                check=models.Q(width_min__gte=0), name="width_min_positive"
            ),
            models.CheckConstraint(
                check=Q(
                    weight_max__gt=F("weight_min"),
                ),
                name="max_weight_gt_min",
            ),
            models.CheckConstraint(
                check=models.Q(weight_max__gte=0), name="weight_max_positive"
            ),
            models.CheckConstraint(
                check=models.Q(weight_min__gte=0), name="weight_min_positive"
            ),
        ]


class EatingType(models.Model):
    """ """

    class EatingCategory(models.TextChoices):
        CARNIVORE = "C", _("Carnivore")
        HERBIVORE = "H", _("Herbivore")
        OMNIVORE = "O", _("Omnivore")

    eating_type = models.CharField(
        max_length=15,
        choices=EatingCategory.choices,
        null=False,
        blank=False,
    )

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.eating_type}"

    class Meta:
        ordering = ["eating_type"]
        constraints = [
            models.UniqueConstraint(fields=["eating_type"], name="unique_eating_type"),
        ]


def image_directory_path(instance, filename):
    """
    where the images will be stored
    """
    folder_name = instance.name
    # period = instance.timestamp # could use also period to further put the image

    return f"images/{folder_name}/{filename}"


class Dinosaur(models.Model):
    """
    A dinosaur is a living thing that lived in the past.
    """

    name = models.CharField(null=False, max_length=250)
    period = models.ForeignKey(Period, null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(DinoSize, null=True, blank=True, on_delete=models.SET_NULL)
    eating_type = models.ForeignKey(
        EatingType, null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.TextField(null=True, blank=True)
    #
    typical_colours = ArrayField(
        models.CharField(
            max_length=12,
            null=True,
        ),
        size=4,
        null=True,
    )

    # TODO add delete images if the dinosaur is deleted
    image1 = models.ImageField(upload_to=image_directory_path, default="img1.jpg")
    image2 = models.ImageField(upload_to=image_directory_path, default="img2.jpg")

    def __str__(self):
        return f"{self.name} : {self.period} : {self.size} : {self.eating_type}"

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_dinosaur_name"),
        ]

class PetDinosaur(models.Model):
    """
    A dinosaur that is a pet.

    Must have a name, a colour, and a diet

    Contraint: we do not want to have two pets with the same name and colour
    because how are we going to tell them apart?
    """

    dino_type = models.ForeignKey(Dinosaur, null=False, blank=False, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=250, null=False)
    age = models.IntegerField(null=False)
    height = models.FloatField(validators=[MinValueValidator(0.001)])
    length = models.FloatField(null=True, validators=[MinValueValidator(0.001)])
    width = models.FloatField(null=True, validators=[MinValueValidator(0.001)])
    weight = models.FloatField(null=True, validators=[MinValueValidator(0.001)])
    colour = models.CharField(max_length=250, null=False)
    diet = models.CharField(max_length=250, null=False)
    pet_description = models.TextField(null=True)

    def __str__(self):
        dino_type = self.dino_type.name
        return f"{self.pet_name} is a {self.colour}  {dino_type} - is a {self.diet}"

    class Meta:
        ordering = ["pet_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["pet_name", "colour"], name="unique_name_colour"
            ),
        ]


class DinoOwner(models.Model):
    """
    An Owner of a dinosaur; only one because imagine if he had more
    But he can like more kinds!
    """

    nickname = models.CharField(max_length=250, default = "awesome dino owner", null=False)
    petDino = models.ForeignKey(
        PetDinosaur, null=True, blank=True, on_delete=models.SET_NULL
    )
    liked_dinosaurs = models.ManyToManyField(Dinosaur, blank=True)

    def __str__(self):
        return f"{self.nickname} owns {self.petDino}"

    class Meta:
        ordering = ["nickname"]
        constraints = [
            models.UniqueConstraint(fields=["nickname"], name="unique_owner_nickname"),
        ]