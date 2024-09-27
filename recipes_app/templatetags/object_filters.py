from django import template
from django.db.models import Avg, Count, Sum

from recipes_app.models import SavedUserDish, DishRating

register = template.Library()


@register.filter
def dish_is_saved(dish, user):
    filtered = SavedUserDish.objects.filter(dish=dish, user=user)
    return filtered.exists()


@register.filter
def average_dish_rating(dish):
    rates = DishRating.objects.filter(dish=dish)
    if rates.exists():
        return rates.aggregate(avg_rate=Avg("rating"))["avg_rate"]
    return "N/A"


@register.filter
def dish_rated(dish, user):
    filtered = DishRating.objects.filter(dish=dish, user=user)
    return filtered.exists()


@register.filter
def average_user_dishes_rating(user):
    queryset = DishRating.objects.filter(dish__created_by=user, rating__isnull=False)
    rates = queryset.aggregate(rates_sum=Sum("rating"))["rates_sum"]
    if rates:
        return round((rates / queryset.count()), 1)
    return "N/A"
