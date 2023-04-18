from django.db import models

# Create your models here.

class Option(models.Model):
    '''Model definition for Option.'''
    option = models.CharField("option", max_length=100)
    
    class Meta:
        '''Meta definition for Option.'''

        verbose_name = 'Option'
        verbose_name_plural = 'Options'

    def __str__(self):
        return self.option[:20]

class Questions(models.Model):
    '''Model definition for Questions.'''
    question = models.CharField("question", max_length=256)
    options = models.ManyToManyField(Option, verbose_name="options",related_name="options")
    answer = models.ManyToManyField(Option, verbose_name="answer",related_name="answer")

    class Meta:
        '''Meta definition for Questions.'''

        verbose_name = 'Questions'
        verbose_name_plural = 'Questionss'

    def __str__(self):
        return self.question[:20]

class Quiz(models.Model):
    '''Model definition for Quiz.'''
    name = models.CharField("name", max_length=150)
    question = models.ManyToManyField(Questions,verbose_name='question',related_name="quiz_question")
    
    class Meta:
        '''Meta definition for Quiz.'''

        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizs'

    def __str__(self):
        return self.name