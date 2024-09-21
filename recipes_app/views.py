from itertools import combinations

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.transaction import commit
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View

from recipes_app.forms import UserLoginForm, RatingForm
from recipes_app.models import Dish, SavedUserDish, DishRating


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base/welcome_page.html")


def registration(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/registration.html")


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "accounts/login.html"
    success_url = "recipes/recipes_list.html"

    def get_success_url(self):
        return reverse("recipes:recipes-list")


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


class SaveRemoveRecipe(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, slug=kwargs["slug"])
        saved_dish = SavedUserDish.objects.filter(dish=dish, user=request.user)
        if saved_dish.exists():
            saved_dish.delete()
        else:
            SavedUserDish.objects.create(dish=dish, user=request.user)
        return redirect(dish.get_absolute_url())
