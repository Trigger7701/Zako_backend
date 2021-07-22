from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework import generics, permissions
from knox.models import AuthToken
from .serializer import *
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth import login
from django.template.loader import get_template
from xhtml2pdf import pisa

def imageUpload(request):
    student = Student.objects.get(id=2)
    file = request.FILES['file']
    student.image = file
    student.save()
    print(student)
    return HttpResponse(file,status=status.HTTP_200_OK)

AuthToken.objects.create(User.objects.get(id=1))
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

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
    # permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def create(self, request, *args, **kwargs):
        # print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            print(type(data.get('image')))
            student = Student.objects.create(full_name=data.get('full_name'),
                                         phone=data.get('phone'),
                                         email=data.get('email'),
                                         age=data.get('age'),
                                         job=data.get('job'),
                                         address=data.get('address'),
                                         image=data.get('image'),
                                         where_know=data.get('where_know'),
                                         description=data.get('description'))
            student.make_student_lesson()
            student.save()
            return Response({"status": "Student Created"}, status=status.HTTP_201_CREATED)
class StudentByGroupViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        if id:
            # group = Group.objects.get(id=)
            student_choises = StudentChoise.objects.filter(group=id)
            queryset = []
            for student_choise in student_choises:
                queryset.append(student_choise.student)
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
        queryset = Payment.objects.all()
        students = Student.objects.all()
        data = []
        for student in students:
            balans = 0
            for pay in queryset.filter(student=student):
                balans += pay.amount
            d = {
                'id':student.id,
                'full_name':student.full_name,
                'balans':balans,
            }
            data.append(d)
        return Response(data)
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        payment = Payment.objects.get(id=id)
        pdf = self.render_to_pdf('check.html', {'payment':payment})
        return pdf
    def render_to_pdf(self,template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

class PaymentByStudentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        payments = Payment.objects.filter(student=id)
        datas = []
        for pay in payments:
            d = {
                'id':pay.id,
                'amount':pay.amount,
                'pay_time':pay.pay_time,
                'admin':pay.admin.user.username,
                'description':pay.description,
                'check':f'http://127.0.0.1:8000/payment/{pay.id}'
            }
            datas.append(d)
        return Response({'image':Student.objects.get(id=id).imageURL,'data':datas})

    def render_to_pdf(self,template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    def update(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            lesson = Lesson.objects.get(id=id)
            if data.get('freezed'):
                lesson.freeze_lesson()
            else:
                lesson.update_lesson(data.get('date'))
            lesson.save()
        return Response({'updated',True})

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=id)
        lesson.freeze_lesson()
        print(id)
        return Response({})



class StudentLessonViewSet(viewsets.ModelViewSet):
    queryset = StudentsLesson.objects.all()
    serializer_class = StudentLessonSerializer
class StudentChoiseViewSet(viewsets.ModelViewSet):
    queryset = StudentChoise.objects.all()
    serializer_class = StudentChoiseSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            student_choise = StudentChoise(
                student = data.get('student'),
                course = data.get('course'),
                group = data.get('group'),
                course_type = data.get('course_type'),
                direction = data.get('direction'),
                claim = data.get('claim'),
                description = data.get('description'),
            )
        student_choise.make_student_lesson()
        student_choise.save()
        return Response({"status": "student coise Created"},status=status.HTTP_200_OK)
    # def destroy(self, request, *args, **kwargs):
    #     id = self.kwargs['pk']
    #     print(id)



class AttantionViewSet(viewsets.ModelViewSet):
    queryset = Attantion.objects.all()
    serializer_class = AttantionSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            attantions = Attantion.objects.filter(group=data.get('group'))
            months = [i.month_num for i in attantions]
            attantion = Attantion.objects.create(
                group = data.get('group')
            )
            if months:
                attantion.month_num = max(months)+1
            if data.get('start_date'):
                attantion.start_date = data.get('start_date')
            else:
                attantion.start_date = attantion.get_last_lesson_date()
            attantion.make_lessons()
            attantion.save()
        return Response({'status':'OK'})
    def retrieve(self, request, *args, **kwargs):
        # try:
            print(self.args,self.kwargs)
            if '-' in self.kwargs['pk']:
                id = int(str(self.kwargs['pk']).split('-')[0])
                att_num = int(str(self.kwargs['pk']).split('-')[1])
            else:
                id = (self.kwargs['pk'])
                att_num = False
            print(id,att_num)
            datas = []
            student_datas = []
            if id:
                group = Group.objects.get(id=id)
                attantions = Attantion.objects.filter(group=group)
                months = [i.month_num for i in attantions]
                if not att_num:
                    att_num = attantions[0].last
                attantion = attantions.get(month_num=att_num)
                lessons = Lesson.objects.filter(attantion_id=attantion.id)
                student_choices = StudentChoise.objects.filter(group=group)
                for lesson in lessons:
                    d = {
                        'dateuid':lesson.id,
                        'key':lesson.id,
                        'date':lesson.date,
                        'freezed':lesson.freezed
                    }
                    print(d)
                    datas.append(d)
                for choice in student_choices:
                    s = dict()
                    s['id']=choice.student.id
                    s['key']=choice.student.id
                    s['full_name']=choice.student.full_name
                    st_lesson = []
                    for lesson in lessons:
                        student_lessons = StudentsLesson.objects.filter(student=choice.student, lesson=lesson)
                        for student_lesson in student_lessons:
                            sl = {
                                'uid':student_lesson.id,
                                'student_id':choice.student.id,
                                'lesson_id':student_lesson.lesson.id,
                                'absence':student_lesson.absence,
                                'key':student_lesson.id
                            }
                            st_lesson.append(sl)
                    s['checkdates'] = st_lesson
                    student_datas.append(s)
            d = {'columns':datas,'data':student_datas,'months':months,'current_month':attantion.last}
                # print(lessons)
            serializer = self.get_serializer(attantion)
            serializer.data.update(d)
            print(d)
            return Response(d)
