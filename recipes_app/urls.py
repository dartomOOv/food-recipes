from django.urls import path
from recipes_app.views import (
    index,
    registration,
    login,
)

urlpatterns = [
    path("", index, name="welcome-page"),
    path("registration/", registration, name="registration-page"),
    path("login", login, name="login-page"),
]
app_name = "recipes"
