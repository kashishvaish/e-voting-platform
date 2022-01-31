from django.urls import path
from admin_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name = 'login.html'), name='admin_login'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'logout.html'), name='admin_logout'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('clear_database', views.clear_database, name = 'clear_database'),
    path('unauthorized', views.unauthorized, name = 'unauthorized'),
]