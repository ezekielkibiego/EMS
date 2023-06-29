
from django.urls import path, include
from empapp import views
# from rest_framework_simplejwt.views import TokenRefreshView
from empapp.views import RegisterView, LoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/employees/', views.employees, name='employees_list'),
    path('api/employees/<str:slug>/', views.employee_detail, name='employee_detail'),
    path('api/profiles/', views.profiles, name='profile'),
    path('api/profiles/<str:username>/', views.user_profile, name='user_profile'),
    path('api/profiles/<str:username>/update/', views.update_user_profile, name='update_user_profile'),

]