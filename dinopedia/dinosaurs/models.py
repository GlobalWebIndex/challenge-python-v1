from django.db import models
from django.db.models import F, Q


class DinoOwner(models.Model):
    name = models.TextField(null=False)

    def __str__(self):
        return self.name


class Period(models.Model):
    """Years are in BC, so the start year is always greater than the end year"""

    name = models.TextField(null=False)
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
