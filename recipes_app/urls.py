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
    IngredientAmountCreateView,
    IngredientCreateView,
    CategoryCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    DishTypeCreateView,
)

urlpatterns = [
    path("", MainPageView.as_view(), name="recipes-list"),
    path("users/<slug:slug>/profile/", ProfileView.as_view(), name="profile"),
    path("users/<slug:slug>/profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("users/<slug:slug>/profile/delete_confirm/", ProfileDeleteView.as_view(), name="profile-delete"),
    path("users/<slug:slug>/saved/", SavedRecipes.as_view(), name="saved_recipes"),
    path("users/<slug:slug>/created/", CreatedRecipes.as_view(), name="created_recipes"),
    path("create/", RecipeCreateView.as_view(), name="recipe-create"),
    path("<slug:slug>/update/", RecipeUpdateView.as_view(), name="recipe-update"),
    path("<slug:slug>/delete/", RecipeDeleteView.as_view(), name="recipe-delete"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("ingredients-amount/create/", IngredientAmountCreateView.as_view(), name="ingredient-amount-create"),
    path("ingredients/create/", IngredientCreateView.as_view(), name="ingredient-create"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("<slug:slug>/save-remove/", SaveRemoveRecipe.as_view(), name="recipe-save-remove"),
]
app_name = "recipes"
