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
    phone = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField(max_length=100, null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    job = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(gettext_lazy('Image'),upload_to=upload_to,null=True,blank=True)
    where_know = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=2000,null=True,blank=True)
    def make_student_lesson(self):
        student_choises = StudentChoise.objects.filter(student=self)
        for student_choise in student_choises:
            if student_choise.group:
                attantions = Attantion.objects.filter(group=student_choise.group)
                for attantion in attantions:
                    lessons = Lesson.objects.filter(attantion=attantion)
                    for lesson in lessons:
                        student_lesson = StudentsLesson(student=self, lesson=lesson)
                        student_lesson.save()
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return self.full_name
class StudentChoise(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    course_type = models.CharField(max_length=100,null=True)
    direction = models.CharField(max_length=100,null=True)
    claim = models.CharField(max_length=1000,null=True)
    description = models.CharField(max_length=1000,null=True)
    def make_student_lesson(self):
        if self.group:
            attantions = Attantion.objects.filter(group=self.group)
            for attantion in attantions:
                lessons = Lesson.objects.filter(attantion=attantion)
                print(f'\n\n\n\n\n\n\n\n{lessons}\n\n\n\n\n\n\n\n\n\n\n')
                for lesson in lessons:
                    student_lesson = StudentsLesson.objects.create(student=self.student, lesson=lesson)
                    student_lesson.save()
    def __str__(self):
        return f'{self.student.full_name} - {self.group.group_name}'


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
    start_date = models.DateField(null=True)
    @property
    def last(self):
        attantions = Attantion.objects.filter(group=self.group)
        if attantions:
            return max([a.month_num for a in attantions])
        else:
            return 1
    def make_lessons(self):
        is_data_null = True
        if self.start_date:
            is_data_null = False
            start_date = self.start_date
        else:
            start_date = Group.objects.get(id=self.group.id).start_date
        one_day = timedelta(days=1)
        odd_days = ['Mon','Wed','Fri']
        even_days = ['Tue','Thu','Sat']
        if start_date.strftime('%a') in odd_days:
            days = odd_days.copy()
        else:
            days = even_days.copy()
        start_date+=one_day
        x = 0
        while x < 12:
            print(x)
            if start_date.strftime('%a') in days:
                print(x+1,start_date)
                lesson=Lesson.objects.create(attantion=self,date=start_date,day_num=x+1)
                lesson.make_for_student()
                lesson.save()
                x += 1
            start_date += one_day
    def __str__(self):
        return f'{self.group} {self.month_num}'
    def get_last_lesson_date(self):
        a = Attantion.objects.filter(group=self.group)
        lessons = Lesson.objects.filter(attantion=a[self.month_num-2])
        # print(lessons,a,self.month_num-1)
        return Lesson.objects.get(id = max([i.id for i in lessons])).date

class Lesson(models.Model):
    attantion = models.ForeignKey(Attantion,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(null=True)
    day_num = models.IntegerField(null=True)
    freezed = models.BooleanField(default=False)
    def __str__(self):
        return f'{"null" if self.attantion == None else str(self.attantion.id)} -> {self.id}'
    def make_for_student(self):
        attantion = Attantion.objects.get(id=self.attantion.id)
        group = Group.objects.get(id = attantion.group.id)
        student_choises = StudentChoise.objects.filter(group=group)
        for student_choise in student_choises:
            student_lesson = StudentsLesson.objects.create(student=student_choise.student,lesson=self)
            student_lesson.save()
    def continue_lesson(self,continue_date):
        one_day = timedelta(days=1)
        odd_days = ['Mon', 'Wed', 'Fri']
        even_days = ['Tue', 'Thu', 'Sat']
        if continue_date.strftime('%a') in odd_days:
            days = odd_days.copy()
        else:
            days = even_days.copy()
        lessons = Lesson.objects.filter(attantion=self.attantion)
        max_id = max([l.id for l in lessons])
        for l in lessons:
            if l.id>=self.id:
                z = True
                while z:
                    if continue_date.strftime('%a') in days:
                        l.date = continue_date
                        l.freezed = False
                        l.save()
                        z = False
                    continue_date += one_day
    def update_lesson(self,date):
        self.freezed = False
        self.date = date
        self.save()
        self.continue_lesson(date)
        lessons = Lesson.objects.filter(attantion=self.attantion)
        max_id = max([l.id for l in lessons])
        sls = StudentsLesson.objects.filter(lesson_id__gte=self.id).filter(lesson_id__lte=max_id)
        for sl in sls:
            sl.absence = 'none'
            sl.save()
    def freeze_lesson(self):
        lessons = Lesson.objects.filter(attantion=self.attantion)
        max_id = max([l.id for l in lessons])
        for l in lessons:
            self.freezed = True
            self.save()
            if l.id>=self.id:
                l.freezed = True
                l.save()
        sls = StudentsLesson.objects.filter(lesson_id__gte=self.id).filter(lesson_id__lte=max_id)
        for sl in sls:
            # print(sl)
            sl.absence = 'freezed'
            sl.save()
    @property
    def current_month_num(self):
        attantions = Attantion.objects.filter(group=self.attantion.group)
        if attantions:
            return max([a.id for a in attantions])
        else:
            return 1
class StudentsLesson(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.SET_NULL,null=True)
    absence = models.CharField(default='none',max_length=10)
    freezed = models.BooleanField(default=False)
    def __str__(self):
        x = ''
        if self.lesson:
            x = f'{self.lesson.date} {self.lesson.attantion.id}'
        return f'{self.student.full_name}: {x}'
