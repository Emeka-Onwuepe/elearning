from django.shortcuts import get_object_or_404

from rest_framework import permissions,generics,status
from rest_framework.response import Response
from article.models import Article
from article.serializer import Get_Article_Serializer
from course.models import Course, Course_Unit
from course.serializers import Get_Course_Serializer, Get_Course_Set_Serializer, Get_Course_Unit_Serializer
from material.models import Material, Video
from material.serializers import Get_Material_Serializer,Get_Video_Serializer
from quiz.models import Quiz
from quiz.serializer import Get_Quiz_Serializer

from school.models import Set, Term

class Get_Courses(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course_sets = {'uniques':None}
        course_ids =[]
        if request.user.user_type == 'student':
            
            student_set =  Set.objects.get(students = request.user)
            if student_set.customize:
                    if not student_set.special_class:
                        content={"Access denied":"You are not assigned to any class."}
                        return Response(content,status=status.HTTP_403_FORBIDDEN)
                    term = Term.objects.get(order= student_set.special_class.term,
                                        term_special_class = student_set.special_class)
            else:
                if not student_set.set_class:
                    content={"Access denied":"You are not assigned to any class."}
                    return Response(content,status=status.HTTP_403_FORBIDDEN)
                term = Term.objects.get(order= student_set.set_class.term,
                                        term_class = student_set.set_class)
                
                
            course_sets_data = Get_Course_Set_Serializer(term.course_set,many=True).data
            course_sets['course_sets'] = course_sets_data
        elif request.user.user_type == 'individual':  
            course_sets_data = Get_Course_Set_Serializer(request.user.course_sets,many=True).data
            course_sets['course_sets'] = course_sets_data
            # courses = Course.objects.filter(pk__in = request.user.courses)
            courses_data = Get_Course_Serializer(request.user.courses,many=True).data
            course_sets['uniques'] = courses_data
            
        for couse_set in course_sets_data:
            for course in couse_set['course_set_unit']:
                course_ids.append(course['course'])
                
        courses = Course.objects.filter(pk__in = course_ids)
        courses_data = Get_Course_Serializer(courses,many=True).data
        course_sets['courses'] = courses_data
        
        return Response(course_sets)
    
class Get_Course(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
  

    def get(self, request, *args, **kwargs):

        course_id = request.query_params['id']
        course = Course.objects.get(id=course_id)
        data = Get_Course_Serializer(course).data
        
        # materials = Material.objects.filter(course_unit__course_week = course.course_week)
        course_units = Course_Unit.objects.filter(course_unit__in = course.course_week.all()).distinct()
        course_unit_data = Get_Course_Unit_Serializer(course_units,many=True).data
        
        materials_id = []
        for item in course_units.values('material'):
            if item['material'] not in materials_id:
                materials_id.append(item['material'])
        material = Material.objects.filter(id__in = materials_id)
        material_data = Get_Material_Serializer(material,many=True).data
        
      
        return Response({'course':data,"units":course_unit_data,'materials':material_data})
    
class Get_Lession(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
  

    def get(self, request, *args, **kwargs):

        lession_id = request.query_params['id']
        type = request.query_params['type']

        if type == 'video':
            lesson = Video.objects.get(id=lession_id)
            lesson_data = Get_Video_Serializer(lesson).data
        if type == 'quiz':
            lesson = Quiz.objects.get(id=lession_id)
            lesson_data = Get_Quiz_Serializer(lesson).data
        if type == 'article':
            lesson = Article.objects.get(id=lession_id)
            lesson_data = Get_Article_Serializer(lesson).data
            
        return Response({'lesson':lesson_data})