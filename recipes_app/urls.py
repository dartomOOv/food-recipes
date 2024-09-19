from django.urls import path
from recipes_app.views import (
    index,
    registration,
    main_page,
    CustomLoginView,
)

urlpatterns = [
    path("", index, name="welcome-page"),
    path("registration/", registration, name="registration-page"),
    path("login", CustomLoginView.as_view(), name="login-page"),
    path("recipes", main_page, name="recipes-list")
]
app_name = "recipes"
