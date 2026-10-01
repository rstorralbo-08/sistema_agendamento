from django.urls import path
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('listar/', views.listar_agendamentos, name='listar'),
    path('novo/', views.novo_agendamento, name='novo'),
    path('editar/<int:pk>/', views.editar_agendamento, name='editar'),
    path('excluir/<int:pk>/', views.excluir_agendamento, name='excluir'),
    path('relatorio/', views.relatorio_agendamentos, name='relatorio'),
]