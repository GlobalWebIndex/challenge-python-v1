from django.contrib import admin

from .models import Dinosaur


@admin.register(Dinosaur)
class DinosaurAdmin(admin.ModelAdmin):
    list_display = ('name', 'colour', 'eating_classification', 'period', 'size', 'image_1', 'image_2')


