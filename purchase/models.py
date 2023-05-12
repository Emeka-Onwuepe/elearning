from django.db import models
from course.models import Course, Course_set

from user.models import User

# Create your models here.
class Purchase(models.Model):
    """Model definition for Purchase."""

    # TODO: Define fields here
    buyer  = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    total = models.IntegerField("total")
    purchase_id = models.CharField("purchase id", max_length=50)
    courses = models.ManyToManyField(Course, verbose_name="courses")
    course_sets = models.ManyToManyField(Course_set, verbose_name="course sets")
    paid = models.BooleanField("paid",default=False)
    date = models.DateField(auto_now=True, auto_now_add=False)
    
    

    class Meta:
        """Meta definition for Purchase."""

        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        ordering = ('date',)

    def __str__(self):
        """Unicode representation of Purchase."""
        return self.purchase_id

    # TODO: Define custom methods here
