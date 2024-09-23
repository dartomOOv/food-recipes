from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from recipes_app.forms import UserLoginForm, RatingForm, CustomRegisterForm, DishCreateForm
from recipes_app.models import Dish, SavedUserDish, DishRating, User, IngredientAmount, Ingredient, Category


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base/welcome_page.html")


class CustomRegisterView(generic.FormView):
    form_class = CustomRegisterForm
    template_name = "accounts/registration.html"

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("login-page")


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "accounts/login.html"
    success_url = "recipes/recipes_list.html"

    def get_success_url(self):
        return reverse_lazy("recipes:recipes-list")


class MainPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.all()
        context = {
            "dishes": dishes
        }

        return render(request, "recipes/recipes_list.html", context=context)


class RecipeDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "recipes/recipe_detail.html"
    model = Dish
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RatingForm()
        context["form"] = form

        return context

    def post(self, request, *args, **kwargs):
        dish_slug = kwargs["slug"]
        dish = get_object_or_404(Dish, slug=dish_slug)
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.dish = dish
            rating.save()
            return redirect(dish.get_absolute_url())
        return redirect(dish.get_absolute_url())


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    template_name = "recipes/recipe_create.html"
    form_class = DishCreateForm
    context_object_name = "form"

    def post(self, request, *args, **kwargs):
        form = DishCreateForm(request.POST)

        if form.is_valid():
            dish = form.save(commit=False)
            dish.created_by = request.user
            dish.save()
            return redirect(dish.get_absolute_url())
        return super().post(self, request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('recipes:recipe-create')


class SaveRemoveRecipe(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, slug=kwargs["slug"])
        saved_dish = SavedUserDish.objects.filter(dish=dish, user=request.user)
        if saved_dish.exists():
            saved_dish.delete()
        else:
            SavedUserDish.objects.create(dish=dish, user=request.user)
        return redirect(dish.get_absolute_url())


class SavedRecipes(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = SavedUserDish.objects.filter(user=request.user).select_related("dish")
        context = {
            "queryset": queryset
        }
        return render(request, "profile/saved_recipes.html", context=context)


class IngredientAmountCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "recipes/ingredient_amount_create.html"
    model = IngredientAmount
    fields = "__all__"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("recipes:recipe-create")


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "recipes/ingredient_create.html"
    model = Ingredient
    fields = "__all__"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("recipes:ingredient-amount-create")


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "recipes/category_create.html"
    model = Category
    fields = "__all__"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("recipes:ingredient-create")


class CreatedRecipes(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(slug=kwargs["slug"])
        dishes = Dish.objects.filter(created_by=user)
        context = {
            "dishes": dishes
        }
        return render(request, "profile/created_recipes.html", context=context)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    slug_field = "slug"
    model = get_user_model()
    template_name = "profile/user_info.html"
    context_object_name = "author"


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    slug_field = "slug"
    model = get_user_model()
    fields = ["username", "first_name", "last_name"]
    template_name = "profile/profile_update.html"
    success_url = reverse_lazy("recipes:profile")

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("recipes:profile", kwargs={"slug": user.slug})

class ProfileDeleteView(LoginRequiredMixin, generic.DeleteView):
    slug_field = "slug"
    model = get_user_model()
    template_name = "profile/delete_confirm.html"

    def get_success_url(self):
        return reverse_lazy("login-page")

