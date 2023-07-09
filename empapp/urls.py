
from django.urls import path, include
from empapp import views
# from rest_framework_simplejwt.views import TokenRefreshView
from empapp.views import RegisterView, LoginView
from .func import UpdateEmployeeProfile, ChangePassword, ChangeEmployeeRoleManager


urlpatterns = [
    path('', views.index, name='index'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/employees/', views.employees, name='employees_list'),
    path('api/employees/<str:slug>/', views.employee_detail, name='employee_detail'),
    path('api/profiles/', views.profiles, name='profile'),
    path('api/profiles/<str:username>/', views.user_profile, name='user_profile'),
    path('api/profiles/update/<str:username>/', views.update_user_profile, name='update_user_profile'),
    path('api/profiles/update-employee/<str:username>/', UpdateEmployeeProfile.as_view(), name='update-employee-profile'),
    path('api/educations/', views.educations, name='educations'),
    path('api/educations/<int:id>/', views.education_detail, name='education_detail'),
    path('api/employee_edu/<int:id>/', views.employee_edu, name='employee_edu'),
    path('api/roles/', views.roles, name='roles'),
    path('api/roles/<int:id>/', views.roles_detail, name='roles_detail'),
    path('api/departs/', views.departs, name='departs'),
    path('api/departs/<int:id>/', views.depart_detail, name='depart_detail'),
    path('api/attendances/', views.attendances, name='attendances'),
    path('api/attendances/<int:id>/', views.attendance_detail, name='attendance_detail'),
    path('api/leaves/', views.leaves, name='leaves'),
    path('api/leaves/<int:id>/', views.leave_detail, name='leave_detail'),
    path('api/performances/', views.performances, name='performances'),
    path('api/performances/<int:id>/', views.perfomance_detail, name='perfomance_detail'),
    path('api/payrolls/', views.payrolls, name='payrolls'),
    path('api/payrolls/<int:id>/', views.pay_detail, name='pay_detail'),
    path('api/trainings/', views.trainings, name='trainings'),
    path('api/trainings/<int:id>/', views.training_detail, name='training_detail'),
    path('api/documents/', views.documents, name='documents'),
    path('api/change_password/<str:username>/', ChangePassword.as_view(), name='change_password'),
    path('api/change_role_manager/<uuid:id>/', ChangeEmployeeRoleManager.as_view(), name='change_role_manager')

]