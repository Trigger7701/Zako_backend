from django.db import models
from django.contrib.auth.models import User
from datetime import date,datetime,timedelta
from django.utils.translation import gettext_lazy

def upload_to(instance,filename):
    return  f'{filename}'

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
    def make_attantion(self):
        att = Attantion.objects.create(group=self)
        att.make_lessons()
        att.save()
    def __str__(self):
        return self.group_name
class Student(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=False)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, null=True)
    image = models.ImageField(gettext_lazy('Image'),upload_to=upload_to,null=True)
    description = models.CharField(max_length=2000,null=True)
    def make_student_lesson(self):
        if self.group:
            attantions = Attantion.objects.filter(group=self.group)
            for attantion in attantions:
                lessons = Lesson.objects.filter(attantion=attantion)
                for lesson in lessons:
                    student_lesson = StudentsLesson(student=self, lesson=lesson)
                    student_lesson.save()


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
class Attantion(models.Model):
    group = models.ForeignKey(Group,null=True,on_delete=models.SET_NULL)
    month_num = models.IntegerField(default=1)
    def make_lessons(self):
        start_date = Group.objects.get(id=self.group.id).start_date
        one_day = timedelta(days=1)
        odd_days = ['Mon','Wed','Fri']
        even_days = ['Tue','Thu','Sat']
        if start_date.strftime('%a') in odd_days:
            days = odd_days.copy()
        else:
            days = even_days.copy()
        x = 0
        while x < 12:
            start_date += one_day
            if start_date.strftime('%a') in days:
                print(x+1,start_date)
                lesson=Lesson.objects.create(attantion=self,date=start_date,day_num=x+1)
                lesson.make_for_student()
                lesson.save()
                x += 1

class Lesson(models.Model):
    attantion = models.ForeignKey(Attantion,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(null=True)
    day_num = models.IntegerField(null=True)
    def __str__(self):
        return 'null' if self.attantion == None else str(self.attantion.id)
    def make_for_student(self):
        attantion = Attantion.objects.get(id=self.attantion.id)
        group = Group.objects.get(id = attantion.group.id)
        students = Student.objects.filter(group=group)
        for student in students:
            student_lesson = StudentsLesson(student=student,lesson=self)
            student_lesson.save()
class StudentsLesson(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.SET_NULL,null=True)
    absence = models.CharField(default='none',max_length=10)
    def __str__(self):
        return f'{self.student.full_name}: {self.lesson.date}'
