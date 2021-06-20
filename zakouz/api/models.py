from django.db import models
from django.contrib.auth.models import User
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True, null=False)
    phone = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, null=True)
    image = models.ImageField(null=True)
    description = models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.full_name
class Teacher(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=False)
    phone = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, null=True)
    image = models.ImageField(null=True)
    specialization = models.CharField(max_length=100,null=False)
    description = models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.full_name
class Course(models.Model):
    course_name = models.CharField(max_length=200,null=False)
    teacher = models.ForeignKey(Teacher,null=True,on_delete=models.SET_NULL)
    price = models.FloatField(default=0)
    def __str__(self):
        return self.course_name
class Group(models.Model):
    group_name = models.CharField(max_length=200,null=False)
    course = models.ForeignKey(Course,default=14, on_delete=models.SET_DEFAULT)
    time = models.TimeField(null=True)
    start_date = models.DateField(null=True)
    def __str__(self):
        return self.group_name
class Student(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=False)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, null=True)
    image = models.ImageField(null=True)
    description = models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.full_name
class Payment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    amount = models.FloatField(null=False)
    pay_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=2000,null=True)
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    def __str__(self):
        return self.student.full_name + ': ' + str(self.amount) + ', ' + str(self.pay_time)


