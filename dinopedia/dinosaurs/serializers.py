from rest_framework import serializers

from dinosaurs.models import Dinosaur, DinoOwner, PetDinosaur


class DinosaurSerializer(serializers.ModelSerializer):

    # liked count and by which owner
    likes_count_by = serializers.SerializerMethodField()

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


    def get_likes_count_by(self, obj):
        """TODO: find something smarter"""
        liked_by = []
        likes_count = 0
        for dinoOwner in DinoOwner.objects.all():
            liked_dinos = dinoOwner.liked_dinosaurs.all()
            for liked_dino in liked_dinos:
                if obj.name in liked_dino.name:
                    likes_count += 1
                    liked_by.append((dinoOwner.id, dinoOwner.nickname,))

        return (likes_count, liked_by,)

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

    # liked_dinosaurs = DinosaurSerializer(many=True)
    number_liked_dinosaurs = serializers.SerializerMethodField()
    class Meta(DinoOwnerSerializerWrite.Meta):
        depth = 1

    def get_number_liked_dinosaurs(self, obj):
        return obj.liked_dinosaurs.count()

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
        owner_data = DinoOwnerSerializerWrite(owner).data
        #Depends on how much detail you want in the response
        # owner_data = DinoOwnerSerializerRead(owner).data
        return owner_data
