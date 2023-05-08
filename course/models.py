from django.db import models

from material.models import Material

# Create your models here.
class Category(models.Model):
    """Model definition for Category."""
    name = models.CharField("name", max_length=150)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

class Course_Unit(models.Model):
    '''Model definition for Course_Unit.'''
    order = models.IntegerField("order")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    
    class Meta:
        '''Meta definition for Course_Unit.'''

        verbose_name = 'Course_Unit'
        verbose_name_plural = 'Course_Units'
        ordering = ['order']

    def __str__(self):
        return f'{self.material} -- {self.order}'
    
class Course_Week(models.Model):
    '''Model definition for Course_Week.'''
    name = models.CharField("name", max_length=150)
    order = models.IntegerField("order")
    course_unit = models.ManyToManyField(Course_Unit, verbose_name="course_unit",
                                         related_name="course_unit")

    class Meta:
        '''Meta definition for Course_Week.'''

        verbose_name = 'Course_Week'
        verbose_name_plural = 'Course_Weeks'
        ordering = ['order']

    def __str__(self):
        return f'{self.name} - {self.order}'
    

class Course(models.Model):
    '''Model definition for Course.'''
    name = models.CharField("name", max_length=250)
    course_week = models.ManyToManyField(Course_Week, verbose_name="course_week",
                                         related_name="course_week"
                                         )
    price = models.FloatField("price",default=0.00)
    public  = models.BooleanField(default=True)
    category = models.ForeignKey(Category, verbose_name="category",
                                 related_name='course_category',
                                 on_delete=models.SET_NULL,null=True)
    purchase_count = models.IntegerField(default=0)
    display_image = models.ImageField("dispaly image", upload_to='display_images/',default='default.jpg')

    class Meta:
        '''Meta definition for Course.'''

        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

class Course_set_unit(models.Model):
    '''Model definition for Course_set_unit.'''
    order = models.IntegerField("order")
    course = models.ForeignKey(Course, verbose_name="course", on_delete=models.CASCADE)

    class Meta:
        '''Meta definition for Course_set_unit.'''

        verbose_name = 'Course_set_unit'
        verbose_name_plural = 'Course_set_units'
        ordering = ['order']

    def __str__(self):
        return f'{self.order} {self.course}'
    
class Course_set(models.Model):
    '''Model definition for Course_set.'''
    name = models.CharField("name", max_length=250)
    course_set_unit = models.ManyToManyField(Course_set_unit, verbose_name="Course set unit",
                                             related_name="course_set_unit")
    price = models.FloatField("price",default=0.00)
    public  = models.BooleanField(default=True)
    category = models.ForeignKey(Category, verbose_name="category", 
                                 related_name='course_set_category',
                                 on_delete=models.SET_NULL,null=True)
    purchase_count = models.IntegerField(default=0)
    display_image = models.ImageField("dispaly image", upload_to='display_images/',default='default.jpg')
    class Meta:
        '''Meta definition for Course_set.'''

        verbose_name = 'Course_set'
        verbose_name_plural = 'Course_sets'

    def __str__(self):
        return self.name 