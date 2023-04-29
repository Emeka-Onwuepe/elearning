from django.db.models.signals import ( post_delete, pre_save)
from django.dispatch import receiver

from article.models import Article, Sections



@receiver(pre_save, sender=Article)
def delete_Artictle_image(sender, instance, *args, **kwargs):
    if instance.pk:
        article = Article.objects.get(pk=instance.pk)
        if article.image != instance.image:
            article.image.delete(False)
        if article.audio != instance.audio:
            article.audio.delete(False)


@receiver(pre_save, sender=Sections)
def delete_Sections_image(sender, instance, *args, **kwargs):
    if instance.pk:
        section = Sections.objects.get(pk=instance.pk)
        if section.Sub_section_image != instance.Sub_section_image:
            section.Sub_section_image.delete(False)
        if section.audio != instance.audio:
            section.audio.delete(False)


@receiver(post_delete, sender=Article)
def delete_artictle_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.audio:
        instance.audio.delete(save=False)

@receiver(post_delete, sender=Sections)
def delete_sections_image(sender, instance, using, *args, **kwargs):
    if instance.Sub_section_image:
        instance.Sub_section_image.delete(save=False)
    if instance.audio:
        instance.audio.delete(save=False)