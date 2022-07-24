from rest_framework import serializers

from dinosaurs.models import Dinosaur


class DinosaurSerializer(serializers.ModelSerializer):

    image1 = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        allow_null=False,
        use_url=True,
        required=False,
    )
    image2 = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        allow_null=False,
        use_url=True,
        required=False,
    )

    class Meta:
        model = Dinosaur
        fields = "__all__"
        depth = 1
        read_only_fields = ["image1", "image2"]

class DinosaurImage1Serializer(serializers.ModelSerializer):   
        class Meta:
            model = Dinosaur
            fields = ["image1"]



class DinosaurImage2Serializer(serializers.ModelSerializer):
        class Meta:
            model = Dinosaur
            fields = ["image2"]
