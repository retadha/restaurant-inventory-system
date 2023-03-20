from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
]