from rest_framework import serializers

from dinosaurs.models import Dinosaur

class DinosaurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dinosaur
        fields = '__all__'
        depth = 1