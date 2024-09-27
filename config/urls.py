"""
URL configuration for config project.

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
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from recipes_app.views import (
    index,
    CustomLoginView,
    CustomRegisterView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="welcome-page"),
    path("recipes/", include("recipes_app.urls", namespace="recipes")),
    path("accounts/login/", CustomLoginView.as_view(), name="login-page"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path(
        "accounts/registration/", CustomRegisterView.as_view(), name="registration-page"
    ),
] + debug_toolbar_urls()
