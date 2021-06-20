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
class StudentByGroupViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def retrieve(self, request, *args, **kwargs):
        print(args,kwargs)
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
        for data in serializer.data:
            d = {'student_name':queryset[0].student.full_name}
            data.update(d)
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