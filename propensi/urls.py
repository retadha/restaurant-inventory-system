from django.contrib import admin
from django.urls import path, include
from login.views import login_page, logout_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('home.urls'), name='index'),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("user/", include('user.urls'), name="user"),
    path('', include('employee.urls')),

]
