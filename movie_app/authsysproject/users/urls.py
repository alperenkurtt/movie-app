from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import logout_view


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('index/', views.index, name='index')
]
