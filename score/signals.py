from django.db.models.signals import ( post_save, pre_save)
from django.dispatch import receiver
from quiz.models import Quiz

from score.models import Course_Score, Quiz_Score

@receiver(pre_save,sender=Course_Score)
def create_Course_Score(sender, instance, *args, **kwargs):
    quiz_count = 0
    course_week = instance.course.course_week.all()
    for week in course_week:
        units = week.course_unit.all().values_list('id',flat=True)
        quiz = Quiz.objects.filter(material_quiz__course_unit__in = units)
        quiz_count+=len(quiz)
    instance.weight =  round(1/quiz_count,2)
        # instance.save(False)
            
@receiver(pre_save,sender=Quiz_Score)
def Update_Course_Score(sender, instance, *args, **kwargs):
    if instance.pk:
        old_instance = Quiz_Score.objects.get(pk = instance.pk)
        daily_limit = 2
        
        if old_instance.current_score != instance.current_score:
            instance.previous_agg_score =  old_instance.agg_score
            instance.daily_count += 1 if instance.daily_count < daily_limit else ((daily_limit*-1)+1)
            instance.attempts += 1
            instance.total +=  instance.current_score
            instance.agg_score = round(instance.total/instance.attempts,2)
            
            diff = instance.agg_score - instance.previous_agg_score
            
            course_score = instance.course_score
            course_score.agg_score = round(course_score.agg_score + (course_score.weight *  diff),2)
            course_score.save()
            
   
   
        
        