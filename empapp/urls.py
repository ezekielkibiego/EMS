from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('edit/<str:coName>', views.edit, name='edit'),
    path('update/<str:coName>', views.update, name='update'),
    path('delete/<str:coName>', views.delete, name='delete'), 
    path('employees', views.employees),
    path('emp', views.emp),
    path('deleteEmp/<str:first_name>', views.deleteEmp),
    path('updateEmp/<str:first_name>', views.updateEmp),
    path('edit/<str:coName>', views.edit),
    

]