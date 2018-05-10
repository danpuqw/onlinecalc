"""online_calc_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from online_calc import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.portal_main, name='main'),
    path('login/', views.DD_login, name='login'),
    path('logout/', views.DD_logout, name='logout'),
    path('save/<int:id>', views.save, name='save'),
    path('register/', views.register, name='register'),
    path('saved_credits/', views.show_credits, name='saved_credits'),
    path('saved_credits/<int:id>', views.show_all, name='show_all'),
    path('saved_credits/delete/<int:id>', views.delete, name='delete'),
]
