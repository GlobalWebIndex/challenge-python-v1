from django.test import TestCase

from dinosaurs.models import *


class DinosaurModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Dinosaur.objects.create(name='T-Rex')

    def test_name_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_eating_classification_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('eating_classification').verbose_name
        self.assertEqual(field_label, 'eating classification')

    def test_colour_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('colour').verbose_name
        self.assertEqual(field_label, 'colour')

    def test_period_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('period').verbose_name
        self.assertEqual(field_label, 'period')

    def test_size_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('size').verbose_name
        self.assertEqual(field_label, 'size')

    def test_image_1_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('image_1').verbose_name
        self.assertEqual(field_label, 'image 1')

    def test_image_2_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('image_2').verbose_name
        self.assertEqual(field_label, 'image 2')

    def test_favorites_label(self):
        dinosaur = Dinosaur.objects.get(id=1)
        field_label = dinosaur._meta.get_field('favorites').verbose_name
        self.assertEqual(field_label, 'favorites')

    def test_name_length(self):
        dinosaur = Dinosaur.objects.get(id=1)
        max_length = dinosaur._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_colour_length(self):
        dinosaur = Dinosaur.objects.get(id=1)
        max_length = dinosaur._meta.get_field('colour').max_length
        self.assertEqual(max_length, 100)

    def test_period_length(self):
        dinosaur = Dinosaur.objects.get(id=1)
        max_length = dinosaur._meta.get_field('period').max_length
        self.assertEqual(max_length, 100)

    def test_size_length(self):
        dinosaur = Dinosaur.objects.get(id=1)
        max_length = dinosaur._meta.get_field('size').max_length
        self.assertEqual(max_length, 100)

    def test_image_1_(self):
        dinosaur = Dinosaur.objects.get(id=1)
        image_1 = dinosaur.image_1
        self.assertEqual(image_1, 'default-dinosaur.png')

    def test_get_absolute_url(self):
        dinosaurs = Dinosaur.objects.get(id=1)
        self.assertEqual(dinosaurs.get_absolute_url(), '/dinosaurs/dinosaur/1')