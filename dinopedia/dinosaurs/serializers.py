from rest_framework import serializers

from dinosaurs.models import Dinosaur, DinoOwner, PetDinosaur


class DinosaurSerializer(serializers.ModelSerializer):

    # add liked_by

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
        # read_only_fields = ["image1", "image2"]


class DinosaurSerializerWrite(DinosaurSerializer):
    class Meta(DinosaurSerializer.Meta):
        depth = 0


class DinosaurImage1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dinosaur
        fields = ["image1"]


class DinosaurImage2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dinosaur
        fields = ["image2"]


class DinoOwnerSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = DinoOwner
        fields = "__all__"


class DinoOwnerSerializerRead(DinoOwnerSerializerWrite):

    liked_dinosaurs = DinosaurSerializer(many=True)
    class Meta(DinoOwnerSerializerWrite.Meta):
        depth = 1


class PetDinosaurSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = PetDinosaur
        fields = "__all__"


class PetDinosaurSerializerRead(PetDinosaurSerializerWrite):

    owner = serializers.SerializerMethodField()

    dino_type = DinosaurSerializer(read_only=True)

    class Meta(PetDinosaurSerializerWrite.Meta):
        depth = 1

    def get_owner(self, obj):
        owner = DinoOwner.objects.filter(petDino=obj).first()
        owner_data = DinoOwnerSerializerRead(owner).data
        return owner_data
