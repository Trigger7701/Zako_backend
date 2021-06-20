from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'teacher',views.TeacherViewSet, basename='index')
router.register(r'course',views.CourseViewSet, basename='course')
router.register(r'group_by_course',views.GroupByCourseViewSet, basename='group_by_course')
router.register(r'group',views.GroupViewSet, basename='group')
router.register(r'student',views.StudentViewSet, basename='student')
router.register(r'student_by_group',views.StudentByGroupViewSet, basename='student_by_group')
router.register(r'payment',views.PaymentViewSet, basename='payment')
router.register(r'payment_by_student',views.PaymentByStudentViewSet, basename='payment_by_student')