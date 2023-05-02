from django.urls import path
from .views import employee_list, employee_detail, create_employee, update_employee, delete_employee

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('<int:employee_id>/', employee_detail, name='employee_detail'),
    path('create/', create_employee, name='create_employee'),
    path('update/<int:employee_id>/', update_employee, name='employee_update'),
    path('delete/<int:employee_id>/', delete_employee, name='employee_delete'),
]