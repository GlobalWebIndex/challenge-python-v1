from django.db import models

# Create your models here.
from django.db import models

class DinoOwner(models.Model):
    name = models.TextField(null=False)

    def __str__(self):
        return self.name