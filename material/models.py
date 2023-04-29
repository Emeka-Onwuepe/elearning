from django.db import models

from article.models import Article
from quiz.models import Quiz

# Create your models here.
class Video(models.Model):
    '''Model definition for Video.'''
    name = models.CharField("name", max_length=150)
    file = models.FileField("file",upload_to = 'videos/',)

    class Meta:
        '''Meta definition for Video.'''

        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.name
    
material_types = (
                ("video","video"),
                ("article","article"),
                ("quiz","quiz"),
                )

class Material(models.Model):
    '''Model definition for Material.'''
    material_type = models.CharField("material_type",choices=material_types, max_length=10)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL,
                              verbose_name="video",related_name="video", 
                              null=True,blank=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL,
                                verbose_name="article",related_name="article",
                                null=True,blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL,
                                verbose_name="quiz",related_name="quiz",
                                null=True,blank=True)


    class Meta:
        '''Meta definition for Material.'''

        verbose_name = 'Material'
        verbose_name_plural = 'Materials'

    def __str__(self):
        if self.video:
            return f'{self.material_type} {self.video}'
        elif self.quiz:
            return f'{self.material_type} {self.quiz}'
        else :
            return f'{self.material_type} {self.article}'