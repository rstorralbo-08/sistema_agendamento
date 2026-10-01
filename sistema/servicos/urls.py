from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('listar/', views.listar_servicos, name='listar'),
    path('novo/', views.novo_servico, name='novo'),
    path('editar/<int:pk>/', views.editar_servico, name='editar'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir'),
    path('status/<int:pk>/', views.alternar_status_servico, name='alternar_status'),
]