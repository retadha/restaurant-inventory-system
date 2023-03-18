from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('home.urls'), name='index'),
    path('', include('employee.urls')),

]
