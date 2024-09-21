from django.urls import path
from recipes_app.views import (
    RecipeDetailView,
    SaveRemoveRecipe,
    MainPageView
)

urlpatterns = [
    path("", MainPageView.as_view(), name="recipes-list"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("<slug:slug>/save/", SaveRemoveRecipe.as_view(), name="recipe-save-remove"),
]
app_name = "recipes"
