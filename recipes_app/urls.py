from django.urls import path
from recipes_app.views import (
    RecipeDetailView,
    SaveRemoveRecipe,
    MainPageView,
    SavedRecipes,
    ProfileView,
    CreatedRecipes,
)

urlpatterns = [
    path("", MainPageView.as_view(), name="recipes-list"),
    path("saved/", SavedRecipes.as_view(), name="saved_recipes"),
    path("created/", CreatedRecipes.as_view(), name="created_recipes"),
    path("<slug:slug>/profile/", ProfileView.as_view(), name="profile"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("<slug:slug>/save/", SaveRemoveRecipe.as_view(), name="recipe-save-remove"),
]
app_name = "recipes"
