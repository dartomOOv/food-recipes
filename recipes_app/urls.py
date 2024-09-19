from django.urls import path
from recipes_app.views import (
    index,
    registration,
    login,
    main_page,
)

urlpatterns = [
    path("", index, name="welcome-page"),
    path("registration/", registration, name="registration-page"),
    path("login", login, name="login-page"),
    path("recipes", main_page, name="recipes-list")
]
app_name = "recipes"
