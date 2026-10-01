from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('listar/', views.listar_clientes, name='listar'),
    path('novo/', views.novo_cliente, name='novo'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar'),
    path('excluir/<int:pk>/', views.excluir_cliente, name='excluir'),
    path('status/<int:pk>/', views.alternar_status_cliente, name='alternar_status')
]