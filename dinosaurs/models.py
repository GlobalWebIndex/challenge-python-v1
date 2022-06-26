from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Dinosaur(models.Model):
    """Model representing a dinosaur"""
    PERIODS_CHOICES = (
        ('triassic', 'triassic'),
        ('jurassic', 'jurassic'),
        ('cretaceous', 'cretaceous'),
        ('paleogene', 'paleogene'),
        ('neogene', 'neogene'),
    )
    SIZE_CHOICES = (
        ('tiny', 'tiny'),
        ('very small', 'very small'),
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large'),
        ('very large', 'very large')
    )
    EATING_CLASS_CHOICES = (
        ('herbivore', 'herbivore'),
        ('omnivore', 'omnivore'),
        ('carnivore', 'carnivore'),
    )
    name = models.CharField(max_length=200, unique=True)
    eating_classification = models.CharField(max_length=100, choices=EATING_CLASS_CHOICES)
    colour = models.CharField(max_length=100)
    period = models.CharField(max_length=100, choices=PERIODS_CHOICES)
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    image_1 = models.ImageField(null=True, blank=True, default='default-dinosaur.png')
    image_2 = models.ImageField(null=True, blank=True)
    favorites = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dinosaur-detail', args=[str(self.id)])

    class Meta:
        ordering = ['id']
        permissions = (("can_edit", "User can create/edit/delete dinosaurs"),)

