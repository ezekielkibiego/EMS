
from django.urls import path, include
from empapp import views
# from rest_framework_simplejwt.views import TokenRefreshView
from empapp.views import RegisterView, LoginView
from .func import UpdateEmployeeProfile


urlpatterns = [
    path('', views.index, name='index'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/employees/', views.employees, name='employees_list'),
    path('api/employees/<str:slug>/', views.employee_detail, name='employee_detail'),
    path('api/profiles/', views.profiles, name='profile'),
    path('api/profiles/<str:username>/', views.user_profile, name='user_profile'),
    path('api/profiles/<str:username>/update/', views.update_user_profile, name='update_user_profile'),
    path('api/profiles/<str:username>/update-employee/', UpdateEmployeeProfile.as_view(), name='update_user_profile'),
    path('api/educations/', views.educations, name='educations'),
    path('api/educations/<int:id>/', views.education_detail, name='education_detail'),
    path('api/employee_edu/<int:id>/', views.employee_edu, name='employee_edu'),
    path('api/roles/', views.roles, name='roles'),
    path('api/departs/', views.departs, name='departs'),
    path('api/attendances/', views.attendances, name='attendances'),
    path('api/leaves/', views.leaves, name='leaves'),
    path('api/performances/', views.performances, name='performances'),
    path('api/payrolls/', views.payrolls, name='payrolls'),
    path('api/trainings/', views.trainings, name='trainings'),
    path('api/documents/', views.documents, name='documents'),

]