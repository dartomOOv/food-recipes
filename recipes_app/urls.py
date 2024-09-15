from django.urls import path
from recipes_app.views import index

urlpatterns = [
    path("", index, name="home-page")
]
app_name = "recipes"
