from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.employee_list, name='employee_list'),
    path('<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('create/', views.create_employee, name='create_employee'),
]