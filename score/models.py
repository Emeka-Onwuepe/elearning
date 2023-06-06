from django.db import models
from course.models import Course
from quiz.models import Quiz

from user.models import User

# Create your models here.
class Course_Score(models.Model):
    """Model definition for Course_Score."""
    
    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE,related_name='user_course_score')
    course = models.ForeignKey(Course, verbose_name="course", on_delete=models.CASCADE,related_name='course_course_score')
    agg_score = models.FloatField(default=0.00)
    weight = models.FloatField(default=0.00)
    
    class Meta:
        """Meta definition for Course_Score."""

        verbose_name = 'Course_Score'
        verbose_name_plural = 'Course_Scores'

    def __str__(self):
        """Unicode representation of Course_Score."""
        return f'{self.agg_score}'
    
    
class Quiz_Score(models.Model):
    """Model definition for Quiz_Score."""

    # TODO: Define fields here
    course_score = models.ForeignKey(Course_Score, verbose_name="Course Score", on_delete=models.CASCADE,related_name='course_score')
    quiz= models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE,related_name='course_score_quiz')
    agg_score =  models.FloatField(default=0.00)
    previous_agg_score =  models.FloatField(default=0.00)
    current_score = models.FloatField(default=0.00)
    attempts = models.IntegerField(default=0.00)
    total = models.FloatField(default=0.00)
    daily_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField("last updated", auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for Quiz_Score."""

        verbose_name = 'Quiz_Score'
        verbose_name_plural = 'Quiz_Scores'

    def __str__(self):
        """Unicode representation of Quiz_Score."""
        return f'{self.total}'


  

