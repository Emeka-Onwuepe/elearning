from django.db.models.signals import ( post_delete, pre_save)
from django.dispatch import receiver

from .models import Video

@receiver(pre_save, sender=Video)
def delete_video_image(sender, instance, *args, **kwargs):
    if instance.pk:
        video = Video.objects.get(pk=instance.pk)
        if video.file != instance.file:
            video.file.delete(False)


@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, using, *args, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

