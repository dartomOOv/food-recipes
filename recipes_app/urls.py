from django.urls import path
from recipes_app.views import (
    RecipeDetailView,
    SaveRemoveRecipe,
    MainPageView,
    SavedRecipes,
    ProfileView,
    CreatedRecipes,
    ProfileUpdateView,
    ProfileDeleteView,
    RecipeCreateView,
)

urlpatterns = [
    path("", MainPageView.as_view(), name="recipes-list"),
    path("user-<slug:slug>/profile/", ProfileView.as_view(), name="profile"),
    path("user-<slug:slug>/profile/update", ProfileUpdateView.as_view(), name="profile-update"),
    path("user-<slug:slug>/profile/delete_confirm", ProfileDeleteView.as_view(), name="profile-delete"),
    path("user-<slug:slug>/saved/", SavedRecipes.as_view(), name="saved_recipes"),
    path("user-<slug:slug>/created/", CreatedRecipes.as_view(), name="created_recipes"),
    path("create/", RecipeCreateView.as_view(), name="recipe-create"),
    path("dish-<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("dish-<slug:slug>/save/", SaveRemoveRecipe.as_view(), name="recipe-save-remove"),
]
app_name = "recipes"
