from django.shortcuts import get_object_or_404

from rest_framework import permissions,generics
from rest_framework.response import Response
from course.models import Course
from course.serializers import Get_Course_Serializer, Get_Course_Set_Serializer

from school.models import Set, Term

class Get_Courses(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course_sets = {'uniques':None}
        course_ids =[]
        if request.user.user_type == 'student':
            
            student_set =  Set.objects.get(students = request.user)
            if student_set.customize:
                term = Term.objects.get(order= student_set.special_class.term,
                                        term_special_class = student_set.special_class)
            else:
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

      
        return Response({'data':data})