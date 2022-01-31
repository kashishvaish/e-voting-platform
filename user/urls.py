from django.urls import path
from user import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('logout', views.logout, name='logout'),
    path('details', views.details, name='details'),
]