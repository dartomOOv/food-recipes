from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from recipes_app.forms import UserLoginForm
from recipes_app.models import Dish


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

@login_required
def main_page(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all()
    context = {
        "dishes": dishes
    }

    return render(request, "recipes/recipes_list.html", context=context)


class RecipeDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "recipes/recipe_detail.html"
    model = Dish
    slug_field = "slug"
