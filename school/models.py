from django.db import models
from django.contrib.auth import get_user_model

from course.models import Course_set
User=get_user_model()

# Create your models here.
class School(models.Model):
    '''Model definition for School.'''
    name = models.CharField("name", max_length=250)
    school_code = models.CharField("school_code", max_length=50)
    email = models.EmailField("email", max_length=30)
    phone  = models.CharField("phone",max_length=20)
    
    class Meta:
        '''Meta definition for School.'''

        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __str__(self):
        return self.name
    
class Class(models.Model):
    '''Model definition for Class.'''
    name = models.CharField("name", max_length=150)
    term = models.IntegerField("term")
    
    class Meta:
        '''Meta definition for Class.'''

        verbose_name = 'Class'
        verbose_name_plural = 'Classs'

    def __str__(self):
        return self.name
    
class Set(models.Model):
    '''Model definition for Set.'''
    name = models.CharField("name", max_length=250)
    school = models.ForeignKey(School, verbose_name="school", on_delete=models.CASCADE)
    set_class = models.ForeignKey(Class, verbose_name="class", on_delete=models.CASCADE)
    student = models.ForeignKey(User, verbose_name="student", related_name="student", on_delete=models.CASCADE)
    
    
    class Meta:
        '''Meta definition for Set.'''

        verbose_name = 'Set'
        verbose_name_plural = 'Sets'

    def __str__(self):
        return self.name
    
class Term(models.Model):
    '''Model definition for Term.'''
    term_class = models.ForeignKey(Class, verbose_name="class", on_delete=models.CASCADE,
                                   related_name='term_class')
    order = models.IntegerField("order")
    course_set = models.ManyToManyField(Course_set, verbose_name="course_set",
                                        related_name='course_set')

    class Meta:
        '''Meta definition for Term.'''

        verbose_name = 'Term'
        verbose_name_plural = 'Terms'

    def __str__(self):
        return f'{self.term_class} -- {self.order}'