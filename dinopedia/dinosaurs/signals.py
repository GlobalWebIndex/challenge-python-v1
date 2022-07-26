from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Dinosaur
import subprocess
from dinopedia.settings import MEDIA_ROOT


@receiver(post_delete, sender=Dinosaur)
def delete_dinosaur_images(sender, instance, using, **kwargs):
    """
    This is triggered after a dinosaur is deleted; it deletes the folder with the images
    """
    # pass # uncomment pass and comment all the other lines when you populate
    dino_name = str(instance.name)
    path_ = f"{MEDIA_ROOT}/images/{dino_name}"

    subprocess.run(["rm", "-rf", path_])
