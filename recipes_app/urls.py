from django.urls import path
from recipes_app.views import (
    main_page,
    RecipeDetailView,
    SaveRemoveRecipe,
)

urlpatterns = [
    path("", main_page, name="recipes-list"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("<slug:slug>/save/", SaveRemoveRecipe.as_view(), name="recipe-save-remove"),
]
app_name = "recipes"
