from django.contrib import admin
from django.urls import path, include
from login.views import login_page, logout_page

urlpatterns = [
    path('admin/', admin.site.urls),  # Jgn lupa buat dikomen pas prod
    path("", include('home.urls'), name='index'),
    path("resep/", include('resep.urls')),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path('employee/', include('employee.urls')),
    path("supplier/", include('supplier.urls')),
]
