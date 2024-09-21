from django.urls import path
from recipes_app.views import (
    RecipeDetailView,
    SaveRemoveRecipe,
    MainPageView,
    SavedRecipes,
)

urlpatterns = [
    path("", MainPageView.as_view(), name="recipes-list"),
    path("saved/", SavedRecipes.as_view(), name="saved_recipes"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("<slug:slug>/save/", SaveRemoveRecipe.as_view(), name="recipe-save-remove"),
]
app_name = "recipes"
