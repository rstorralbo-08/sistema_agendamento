"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView  # 1. Importar as views nativas

urlpatterns = [
    path('admin/', admin.site.urls),
    # Autenticação nativa
    path('login/', LoginView.as_view(), name='login'),
    # No Django 4+, LogoutView funciona via POST ou GET dependendo da versão, 
    # sendo recomendado POST por segurança
    path('logout/', LogoutView.as_view(), name='logout'),

    # Rotas dos seus apps (exemplo)
    path('', include('core.urls')), # Onde ficará o dashboard
    path('clientes/', include('clientes.urls')),
    path('servicos/', include('servicos.urls')),
    path('agendamento/', include('agendamento.urls')),
]
