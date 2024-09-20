from django.urls import path
from recipes_app.views import (
    registration,
    main_page,
    CustomLoginView,
    RecipeDetailView,
)

urlpatterns = [
    path("registration/", registration, name="registration-page"),
    path("login", CustomLoginView.as_view(), name="login-page"),
    path("", main_page, name="recipes-list"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
]
app_name = "recipes"
