from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:

    return render(request, "base/welcome_page.html")

def registration(request: HttpRequest) -> HttpResponse:

    return render(request, "accounts/registration.html")

def login(request: HttpRequest) -> HttpResponse:

    return render(request, "accounts/login.html")
