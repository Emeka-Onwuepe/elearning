from rest_framework import permissions,generics
from rest_framework.response import Response
from quiz.models import Quiz
from quiz.serializer import Get_Quiz_Serializer
from score.models import Course_Score, Quiz_Score
from score.serializer import Get_Course_Score_Serializer, Get_Quiz_Score_Serializer


class Get_Quiz_Score(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):

        param = request.query_params
        user = request.user
        quiz_id = param['quiz_id']
        course_id = param['course_id']
        
        quiz_score = Quiz_Score.objects.get(quiz=int(quiz_id),
                                            course_score__user=user,
                                            course_score__course=int(course_id))
        
        data = Get_Quiz_Score_Serializer(quiz_score).data
        return Response(data)  
    
class Get_Course_Score(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):

        user = request.user
        course_id = request.query_params['course_id']
        
        quiz_score = Course_Score.objects.get(user=user,course=int(course_id))
        
        data = Get_Course_Score_Serializer(quiz_score).data
        return Response(data)  

class Quiz_View(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):

        quiz_id = request.query_params['id']
        quiz = Quiz.objects.get(pk = int(quiz_id))
        quiz = Get_Quiz_Serializer(quiz).data
        
        return Response(quiz)  
    
    def post(self, request, *args, **kwargs):

        user = request.user
        data = request.data
        
        if data['quiz_score_id']:
            quiz_score = Quiz_Score.objects.get(pk=int(data['quiz_score_id']))
            quiz_score.current_score = float(data['score'])
            quiz_score.save()
            updated = Get_Quiz_Score_Serializer(quiz_score).data
        else: 
            # quiz = Quiz.objects.get(pk = int(data['quiz_id']))
            course_score,_= Course_Score.objects.get_or_create(user=user.id,course=data['course_id']) 
            quiz_score,_= Quiz_Score.objects.get_or_create(course_score=course_score,quiz=int(data['quiz_id'])) 
            quiz_score.current_score = float(data['score'])
            quiz_score.save()
            updated = Get_Quiz_Score_Serializer(quiz_score).data
        
        return Response(updated)  
    
