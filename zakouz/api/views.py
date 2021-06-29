from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.shortcuts import get_object_or_404
from .serializer import *
from django.http import Http404
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date,datetime
import json
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            print(data)
            group = Group.objects.create(group_name=data.get('group_name'),
                                         time=data.get('time'),
                                         course=data.get('course'),
                                         start_date=data.get('start_date'))
            group.make_attantion()
            group.save()
            return Response({"status": "Group Created"}, status=status.HTTP_201_CREATED)
class GroupByCourseViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    def retrieve(self, request, *args, **kwargs):
        print(args,kwargs)
        id = self.kwargs['pk']
        print(id)
        if id:
            queryset = Group.objects.filter(course=id)
            print(queryset)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            print(data)
            student = Student.objects.create(full_name=data.get('full_name'),
                                         group=data.get('group'),
                                         phone=data.get('phone'),
                                         email=data.get('email'),
                                         image=data.get('image'),
                                         description=data.get('description'))
            student.make_student_lesson()
            student.save()
            return Response({"status": "Student Created"}, status=status.HTTP_201_CREATED)
class StudentByGroupViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        print(id)
        if id:
            queryset = Student.objects.filter(group=id)
            print(queryset)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def list(self, request, *args, **kwargs):
        id = self.request.query_params.get("id", None)
        if id is None:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.get(pk=id)
        serializer = self.get_serializer(queryset, many=True)
        i=0
        for data in serializer.data:
            d = {'student_name':queryset[i].student.full_name}
            data.update(d)
            i+=1
        return Response(serializer.data)
class PaymentByStudentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        queryset = Payment.objects.filter(student=id)
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            d = {'student_name':queryset[0].student.full_name}
            data.update(d)
        return Response(serializer.data)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
class StudentLessonViewSet(viewsets.ModelViewSet):
    queryset = StudentsLesson.objects.all()
    serializer_class = StudentLessonSerializer
class AttantionViewSet(viewsets.ModelViewSet):
    queryset = Attantion.objects.all()
    serializer_class = LessonSerializer
    def retrieve(self, request, *args, **kwargs):
        try:
            print(self.args,self.kwargs)
            id = int(str(self.kwargs['pk']).split(',')[0])
            print(id)
            datas = []
            student_datas = []
            if id:
                group = Group.objects.get(id=id)
                attantion = Attantion.objects.get(group=group)
                lessons = Lesson.objects.filter(attantion_id=attantion.id)
                students = Student.objects.filter(group=group)
                for lesson in lessons:
                    d = dict()
                    d['dateuid'] = lesson.id
                    d['key'] = lesson.id
                    d['date'] = lesson.date
                    print(d)
                    datas.append(d)
                for student in students:
                    s = dict()
                    s['id']=student.id
                    s['key']=student.id
                    s['full_name']=student.full_name
                    student_lessons = StudentsLesson.objects.filter(student=student)
                    st_lesson = []
                    for student_lesson in student_lessons:
                        sl = dict()
                        sl['uid'] = student_lesson.id
                        sl['student_id'] = student.id
                        sl['lesson_id'] = student_lesson.lesson.id
                        sl['absence'] = student_lesson.absence
                        sl['key'] = student_lesson.id
                        st_lesson.append(sl)
                    s['checkdates'] = st_lesson
                    student_datas.append(s)
            d = {'columns':datas,'data':student_datas}
                # print(lessons)
            serializer = self.get_serializer(attantion)
            serializer.data.update(d)
            print(d)
            return Response(d)
        except Exception as e:
            return Response({'error':"404 or 500"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)