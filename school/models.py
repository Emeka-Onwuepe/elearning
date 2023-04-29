from django.db import models
from django.contrib.auth import get_user_model

from course.models import Course_set
User=get_user_model()

# Create your models here.
class School(models.Model):
    '''Model definition for School.'''
    name = models.CharField("name", max_length=250,unique=True)
    school_code = models.CharField("school_code", max_length=50,null=True,blank=True)
    email = models.EmailField("email", max_length=30,null=True,blank=True)
    phone  = models.CharField("phone",max_length=20,null=True,blank=True)
    customize = models.BooleanField("customize",default= False)
    school_link =  models.CharField("school_link", max_length=100,null=True,blank=True)
    latest_set = models.DateField("latest_set", auto_now=False, auto_now_add=False)
    
    
    class Meta:
        '''Meta definition for School.'''

        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __str__(self):
        return self.name
    
class Class(models.Model):
    '''Model definition for Class.'''
    name = models.CharField("name", max_length=150)
    term = models.IntegerField("term",default=0)
    
    class Meta:
        '''Meta definition for Class.'''

        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        ordering = ['id']

    def __str__(self):
        return self.name

class SpecialClass(models.Model):
    '''Model definition for SpecialClass.'''
    name = models.CharField("name", max_length=150)
    term = models.IntegerField("term",default=0)
    
    class Meta:
        '''Meta definition for SpecialClass.''' 

        verbose_name = 'SpecialClass'
        verbose_name_plural = 'SpecialClasses'
        ordering = ['id']

    def __str__(self):
        return self.name
    
class Set(models.Model):
    '''Model definition for Set.'''
    name = models.CharField("name", max_length=250)
    school = models.ForeignKey(School, verbose_name="school", on_delete=models.CASCADE)
    set_class = models.ForeignKey(Class, verbose_name="class", on_delete=models.CASCADE,null=True,blank=True)
    special_class = models.ForeignKey(SpecialClass, verbose_name="Special class", 
                                        on_delete=models.SET_NULL,null=True,blank=True)
    students = models.ManyToManyField(User, verbose_name="student", related_name="student")
    customize = models.BooleanField("customize",default= False)
    
    
    class Meta:
        '''Meta definition for Set.'''

        verbose_name = 'Set'
        verbose_name_plural = 'Sets'

    def __str__(self):
        return self.name
    
class Term(models.Model):
    '''Model definition for Term.'''
    term_class = models.ForeignKey(Class, verbose_name="class", on_delete=models.CASCADE,
                                   related_name='term_class',null=True,blank=True)
    term_special_class = models.ForeignKey(SpecialClass, verbose_name="special_class", on_delete=models.SET_NULL,
                                   related_name='term_special_class',null=True,blank=True)
    order = models.IntegerField("order")
    course_set = models.ManyToManyField(Course_set, verbose_name="course_set",
                                        related_name='course_set')

    class Meta:
        '''Meta definition for Term.'''

        verbose_name = 'Term'
        verbose_name_plural = 'Terms'

    def __str__(self):
        if self.term_class:
            return f'{self.term_class} -- {self.order}'
        elif self.term_special_class:
            return f'{self.term_special_class} -- {self.order}'
