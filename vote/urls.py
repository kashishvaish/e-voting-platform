from django.urls import path
from vote import views

urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('access_denied', views.access_denied, name='access_denied')
]