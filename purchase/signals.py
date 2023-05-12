from django.db.models.signals import ( post_save, pre_save)
from django.dispatch import receiver

from purchase.models import Purchase
from school.models import User

@receiver(post_save,sender=Purchase)
def add_school(sender, instance, *args, **kwargs):
    user =instance.buyer
    if instance.paid:
        for course in instance.courses.all():
            user.courses.add(course)
        for course_set in instance.course_sets.all():
            user.course_sets.add(course_set)
    elif not instance.paid:
        for course in instance.courses.all():
            user.courses.remove(course)
        for course_set in instance.course_sets.all():
            user.course_sets.remove(course_set)
        