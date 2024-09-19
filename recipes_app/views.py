from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from recipes_app.models import Dish


def index(request: HttpRequest) -> HttpResponse:

    return render(request, "base/welcome_page.html")

def registration(request: HttpRequest) -> HttpResponse:

    return render(request, "accounts/registration.html")

def login(request: HttpRequest) -> HttpResponse:

    return render(request, "accounts/login.html")

def main_page(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all()
    context = {
        "dishes": dishes
    }

    return render(request, "recipes/recipes_list.html", context=context)

