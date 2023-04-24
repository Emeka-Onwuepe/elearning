from random import random
from re import findall

from django.db.models.signals import (pre_delete,m2m_changed,
                                        post_save, pre_save)
from django.dispatch import receiver

from .models import School,Set,Class,Term,SpecialClass
from elearning.settings import CORS_ORIGIN_WHITELIST

@receiver(pre_save,sender=School)
def add_school(sender, instance, *args, **kwargs):
    if instance.school_code:
        pass
    else:
        year = str(instance.latest_set.year)
        rand_num = str(random())[-5:]
        split_name = instance.name.split(' ')
        abbr = ""
        for word in split_name:
            if word:
                # avoid empty strings
                abbr += word[0].upper()

        name = instance.name[:5]
        instance.school_code = f"{abbr}{year}{rand_num}"
        instance.school_link = f'{CORS_ORIGIN_WHITELIST[0]}/register/{instance.school_code}'

@receiver(post_save,sender=School)
def add_school(sender, instance, *args, **kwargs):
    
    year = instance.latest_set.year
    default_classes = [
                    "kg_1","kg_2",
                    "primary_1","primary_2","primary_3",
                     "primary_4","primary_5","primary_6"
                     ]
    length = len(default_classes)
    default_sets = [None] * length
    for index in range(length):
        default_sets[index] = f'{year-index}_set'
   
    for index in range(length):
        if instance.customize:
            abbr = findall('[A-Z]+', instance.school_code)[0]
            name = f'{abbr}_{default_classes[index]}'
            new_specialclass, created = SpecialClass.objects.get_or_create(name = name )
            new_set, created = Set.objects.get_or_create(name = default_sets[index],
                                                            school = instance)
            new_set.customize = True
            new_set.set_class = None
            new_set.special_class = new_specialclass
            new_set.save()

            for num in range(1,4):
                new_term,created = Term.objects.get_or_create(term_special_class=new_specialclass,order=num)
                new_term.term_class = None
                new_term.save()

        else:

            new_class, created = Class.objects.get_or_create(name = default_classes[index] )
            new_set, created = Set.objects.get_or_create(name = default_sets[index],
                                                            school = instance)
            new_set.customize = False
            new_set.special_class = None
            new_set.set_class = new_class
            new_set.save()

            for num in range(1,4):
                new_term,created = Term.objects.get_or_create(term_class=new_class,order=num)
                new_term.term_special_class = None
                new_term.save()



    



