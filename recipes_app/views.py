from venv import create

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from recipes_app.forms import (
    UserLoginForm,
    RatingForm,
    CustomRegisterForm,
    DishCreateForm,
    DishSearchForm,
)
from recipes_app.models import (
    Dish,
    SavedUserDish,
    IngredientAmount,
    Ingredient,
    Category,
    DishType,
)


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


class MainPageView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "recipes/recipes_list.html"
    context_object_name = "dishes"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


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
    template_name = "recipes/recipe_form.html"
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
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("recipes:recipe-create")


class RecipeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    template_name = "recipes/recipe_form.html"
    slug_field = "slug"
    form_class = DishCreateForm
    context_object_name = "form"


class RecipeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "recipes/recipe_delete.html"

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("recipes:created_recipes", kwargs={"slug": user.slug})


class SaveRemoveRecipe(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, slug=kwargs["slug"])
        saved_dish = SavedUserDish.objects.filter(dish=dish, user=request.user)
        if saved_dish.exists():
            saved_dish.delete()
        else:
            SavedUserDish.objects.create(dish=dish, user=request.user)
        return redirect(dish.get_absolute_url())


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


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "recipes/dish_type_create.html"
    model = DishType
    fields = "__all__"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("recipes:recipe-create")


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "recipes/category_create.html"
    model = Category
    fields = "__all__"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("recipes:ingredient-create")


class SavedRecipes(LoginRequiredMixin, generic.ListView):
    model = SavedUserDish
    template_name = "profile/saved_recipes.html"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SavedRecipes, self).get_context_data(**kwargs)
        queryset = SavedUserDish.objects.filter(user=self.request.user)
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        is_paginated = paginator.num_pages > 1
        context["queryset"] = queryset
        context["is_paginated"] = is_paginated
        return context


class CreatedRecipes(LoginRequiredMixin, View):
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(slug=kwargs["slug"])
        dishes = Dish.objects.filter(created_by=user).select_related("created_by")
        paginator = Paginator(dishes, self.paginate_by)

        pages = request.GET.get("page")

        try:
            page_obj = paginator.page(pages)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        is_paginated = paginator.num_pages > 1

        context = {
            "page_obj": page_obj,
            "slug": kwargs["slug"],
            "is_paginated": is_paginated
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
