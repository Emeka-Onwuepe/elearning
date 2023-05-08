from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,PermissionsMixin)

from course.models import Course, Course_Unit, Course_set

# Create your models here.

user_types = (
                ("student","student"),
                ("individual","individual"),
                )

class UserManager(BaseUserManager):
    def create_user(self,email, 
                    first_name='null',last_name='null',
                    user_type="individual",phone_number=None,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,last_name=last_name,
                          user_type=user_type,phone_number=phone_number
                           )
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_superuser(self, email, password):
        user = self.create_user(email,password=password,first_name="SITE",last_name="CREATOR",)
        user.is_admin = True
        user.staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    first_name =models.CharField(verbose_name='first name', max_length=255)
    last_name =models.CharField(verbose_name='last name', max_length=255)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    user_type = models.CharField(max_length=10, choices = user_types)
    phone_number = models.CharField(verbose_name='phone number', max_length=20,null=True,blank=True)
    completed_course_units = models.ManyToManyField(Course_Unit, verbose_name="completed_course_units",
                                                   related_name='completed_course_units')
    completed_courses = models.ManyToManyField(Course, verbose_name="completed_courses",
                                                   related_name='completed_courses')
    completed_course_sets = models.ManyToManyField(Course_set, verbose_name="completed_course_sets",
                                                   related_name='completed_course_sets')
    courses = models.ManyToManyField(Course, verbose_name="courses",
                                                   related_name='user_courses')
    course_sets = models.ManyToManyField(Course_set, verbose_name="course_sets",
                                                   related_name='user_course_sets')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_general_admin = models.BooleanField(default=False)
    is_double = models.BooleanField(default=False)
    staff=models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        if not self.is_admin and self.staff:
            if perm =="Users.add_user" or perm=="Users.change_user" or perm=="Users.delete_user":
                return False
            else:
                return True
        else:
            return True

    # remember to set appropriate permissions.
    def has_module_perms(self, app_label):
        if not self.is_admin and self.staff:
            if app_label =="knox" or app_label=="auth" :
                return False
            else:
                return True
        else:
            return True
    @property

    def is_staff(self):
        return self.staff


