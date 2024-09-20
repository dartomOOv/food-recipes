from django.urls import path
from recipes_app.views import (
    index,
    registration,
    main_page,
    CustomLoginView,
)

urlpatterns = [
    path("registration/", registration, name="registration-page"),
    path("login", CustomLoginView.as_view(), name="login-page"),
    path("", main_page, name="recipes-list")
]
app_name = "recipes"
