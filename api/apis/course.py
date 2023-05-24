from django.shortcuts import get_object_or_404

from rest_framework import permissions,generics,status
from rest_framework.response import Response
from article.models import Article
from article.serializer import Get_Article_Serializer
from course.models import Category, Course, Course_Unit,Course_set
from course.serializers import Get_Category, Get_Course_Serializer, Get_Course_Set_Serializer, Get_Course_Set_Serializer_Depth, Get_Course_Unit_Serializer
from material.models import Material, Video
from material.serializers import Get_Material_Serializer,Get_Video_Serializer
from quiz.models import Quiz
from quiz.serializer import Get_Quiz_Serializer

from school.models import Set, Term
from django.conf import settings

class Get_Courses(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        returned_data = {
                        'uniques':[],
                       'course_sets': [],
                       'course': [],
                       'public_key': None,
                        # 'categories': [],
                        'available_courses': []
                       }
        course_ids =[]
        course_sets_id = []
        course_sets_data = []
        term = None
        if request.user.user_type == 'student':
            
            student_set =  Set.objects.get(students = request.user)
            if student_set.customize:
                    if not student_set.special_class and not request.user.is_double:
                        content={"Access denied":"You are not assigned to any class."}
                        return Response(content,status=status.HTTP_403_FORBIDDEN)
                    if student_set.special_class:
                        term = Term.objects.get(order= student_set.special_class.term,
                                        term_special_class = student_set.special_class)
            else:
                if not student_set.set_class and not request.user.is_double:
                    content={"Access denied":"You are not assigned to any class."}
                    return Response(content,status=status.HTTP_403_FORBIDDEN)
                if student_set.set_class:
                    term = Term.objects.get(order= student_set.set_class.term,
                                        term_class = student_set.set_class)
                
            if term: 
                course_sets_data = Get_Course_Set_Serializer(term.course_set,many=True).data
                returned_data['course_sets'].extend(course_sets_data)
        if request.user.user_type == 'individual' or request.user.is_double:  
            course_sets_data = Get_Course_Set_Serializer(request.user.course_sets,many=True).data
            if course_sets_data:
                returned_data['course_sets'].extend(course_sets_data)
            # courses = Course.objects.filter(pk__in = request.user.courses)
            courses_data = Get_Course_Serializer(request.user.courses,many=True).data
            if courses_data:
                returned_data['uniques'].extend(courses_data) 
            
            
        for course_set in returned_data['course_sets']:
            course_sets_id.append(course_set['id'])
            for course in course_set['course_set_unit']:
                course_ids.append(course['course'])
                
        for course in returned_data['uniques']:
            course_ids.append(course['id'])
                
        courses = Course.objects.filter(pk__in = course_ids)
        courses_data = Get_Course_Serializer(courses,many=True).data
        returned_data['courses'] = courses_data
        
        # this part is not scaleable
        # change as the application grows
        # course_sets = []
        # single_courses = []
        available_courses = []
        # purchase_count
        # public
        # category
        
        if request.user.user_type == 'individual' or request.user.is_double: 
            categories = Category.objects.all()
            # returned_data['categories'] = Get_Category(categories,many=True).data
            
            for category in categories:
                category_data = {
                        "category":category.name,
                        'category_id': category.id,
                        'singles':[],
                         'course_sets':[]}
                course_set = Course_set.objects.exclude(pk__in=course_sets_id).filter(category=category,
                                                    public = True).order_by('purchase_count')[:10]
                course_set = Get_Course_Set_Serializer_Depth(course_set,many=True).data
                if course_set:
                    # course_sets.append(course_set)
                    category_data['course_sets'] = course_set
                
                singles = Course.objects.exclude(pk__in=course_ids).filter(category=category,
                                                    public = True).order_by('purchase_count')[:10]
                singles = Get_Course_Serializer(singles,many=True).data
                if singles:
                    # single_courses.append(singles)
                    category_data['singles'] = singles
                if category_data['singles'] or category_data['course_sets'] :
                    available_courses.append(category_data)
                
            # returned_data['available_course_set'] = course_sets
            # returned_data['available_singles'] = single_courses
            returned_data['available_courses'] = available_courses
            returned_data['public_key'] = settings.PAYSTACT_PUBLIC_KEY
        
        # personal_course_set = 
              
        return Response(returned_data)
    
class Get_Category(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        name = request.query_params['name']
        id = request.query_params['id']
        
        course_sets_id = []
        course_ids = []
        course_set_list  = []
    
        term = None
        if request.user.user_type == 'student':
            
            student_set =  Set.objects.get(students = request.user)
            if student_set.customize:
                    if not student_set.special_class and not request.user.is_double:
                        content={"Access denied":"You are not assigned to any class."}
                        return Response(content,status=status.HTTP_403_FORBIDDEN)
                    if student_set.special_class:
                        term = Term.objects.get(order= student_set.special_class.term,
                                        term_special_class = student_set.special_class)
            else:
                if not student_set.set_class and not request.user.is_double:
                    content={"Access denied":"You are not assigned to any class."}
                    return Response(content,status=status.HTTP_403_FORBIDDEN)
                if student_set.set_class:
                    term = Term.objects.get(order= student_set.set_class.term,
                                        term_class = student_set.set_class)
                
            if term: 
                course_set_list.extend(term.course_set.all())
            
        course_set_list.extend(request.user.course_sets.all()) 
        course_ids.extend(request.user.courses.all().values_list('id',flat=True))
        
        for course_set in course_set_list:
            course_sets_id.append(course_set.id)
            for course in course_set.course_set_unit.all():
                course_ids.append(course.course.id)
      
        
        category = Category.objects.get(pk=id,name=name)
        course_sets = Course_set.objects.filter(category=category).exclude(pk__in = course_sets_id)
        courses = Course.objects.filter(category=category).exclude(pk__in = course_ids)
        course_sets = Get_Course_Set_Serializer_Depth(course_sets,many=True).data
        courses = Get_Course_Serializer(courses,many=True).data
        
        return Response({"course_sets":course_sets,"courses":courses})   
        
        
        
    
    
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