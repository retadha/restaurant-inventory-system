from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.create_employee, name='create_employee'),
]