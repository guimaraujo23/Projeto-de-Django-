from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.painel, name='painel'),
    path('deletar/<int:pk>/', views.deletar_transacao, name='deletar_transacao'),
    path('editar/<int:pk>/', views.editar_transacao, name='editar_transacao'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]