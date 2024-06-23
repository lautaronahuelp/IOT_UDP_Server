from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_comandos, name='lista_comandos'),
    path('comando/<int:pk>/', views.envia_comando, name='envia_comando'),
]