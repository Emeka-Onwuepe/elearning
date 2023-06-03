from django.contrib import admin

from score.models import Course_Score, Quiz_Score

# Register your models here.
class CourseScoreAdmin(admin.ModelAdmin):
    list_display = ("user","course",'agg_score')
    
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('id',"quiz","agg_score",'previous_agg_score')
    
admin.site.register(Course_Score,CourseScoreAdmin)
admin.site.register(Quiz_Score,QuizScoreAdmin)