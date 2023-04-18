from django.db import models

from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
# from django.utils import timezone
import datetime
import re
from PIL import Image
from math import floor
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(default="null")
    audio = models.FileField("audio",null=True, blank=True)
    image = models.ImageField(null=True)
    image_source = models.CharField(max_length=255, null=True, blank=True)
    image_description = models.CharField(
        max_length=255, default='image', blank=True)
    sub_heading = models.CharField(max_length=255, null=True, blank=True)
    body_text = RichTextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(null=True)
    publish = models.BooleanField(default=False)
    references = RichTextField(default="null", null=True, blank=True)

    def bodySnippet(self):
        body = self.body_text[:120]
        bodySnippet = re.sub(
            r"\s\w+$|(<strong>|</strong>|<em>|</em>|<b>|</b>|<i>|</i>|<u>|</u>|<a.+?>|</a>)", "", body)
        return f'{bodySnippet} ....'

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-pub_date']
        

    def save(self, skip_md=True, *args, **kwargs):
        if skip_md:
            self.mod_date = datetime.datetime.now()

        if self.image:
            im = Image.open(self.image)
            width, height = im.size
            output = BytesIO()
            n = 0.5
            Width = floor(width * n)
            Height = floor(height * n)
            if width > 1000:
                im = im.resize((Width, Height))
                im.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split(
                    '.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)  # Call the real save() method


class Sections(models.Model):
    """Model definition for Sections."""
    # TODO: Define fields here
    article = models.ForeignKey(
        Article, related_name='sections', on_delete=models.CASCADE)
    sub_heading = models.CharField(max_length=255, null=True)
    audio = models.FileField("audio",null=True, blank=True)
    Sub_section_image = models.ImageField(null=True, blank=True)
    image_source = models.CharField(max_length=255, null=True, blank=True)
    image_description = models.CharField(
        max_length=255, default="image", blank=True)
    body_text = RichTextField(null=True)

    class Meta:
        """Meta definition for Sections."""
        verbose_name = 'Sections'
        verbose_name_plural = 'Sections'

    def __str__(self):
        """Unicode representation of Sections."""
        return self.sub_heading

    def save(self, *args, **kwargs):
        if self.Sub_section_image:
            im = Image.open(self.Sub_section_image)
            width, height = im.size
            output = BytesIO()
            n = 0.5
            Width = floor(width * n)
            Height = floor(height * n)
            if width > 1000:
                im = im.resize((Width, Height))
                im.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.Sub_section_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.Sub_section_image.name.split('.')[
                                                              0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)  # Call the real save() method


@receiver(pre_save, sender=Article)
def delete_Artictle_image(sender, instance, *args, **kwargs):
    if instance.pk:
        article = Article.objects.get(pk=instance.pk)
        if article.image != instance.image:
            article.image.delete(False)


@receiver(pre_save, sender=Sections)
def delete_Sections_image(sender, instance, *args, **kwargs):
    if instance.pk:
        section = Sections.objects.get(pk=instance.pk)
        if section.Sub_section_image != instance.Sub_section_image:
            section.Sub_section_image.delete(False)


@receiver(post_delete, sender=Article)
def delete_artictle_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=Sections)
def delete_sections_image(sender, instance, using, *args, **kwargs):
    if instance.Sub_section_image:
        instance.Sub_section_image.delete(save=False)
