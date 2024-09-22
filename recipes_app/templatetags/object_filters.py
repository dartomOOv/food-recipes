from django import template
from django.db.models import Avg, Count

from recipes_app.models import SavedUserDish, DishRating, CreatedUserDish

register = template.Library()


@register.filter
def join_authors(user_dishes):
    return ", ".join(
        [user_dish.user.username for user_dish in user_dishes.all().select_related("user")]
    )


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
def total_dishes(user):
    dishes = CreatedUserDish.objects.filter(user=user)
    return dishes.aggregate(total=Count("dish"))["total"]

@register.filter
def average_user_dishes_rating(user):
    total = None
    queryset = CreatedUserDish.objects.filter(user=user)
    for query in queryset.select_related("dish"):
        if total:
            total += DishRating.objects.filter(dish=query.dish)
        else:
            total = DishRating.objects.filter(dish=query.dish)
    if total:
        if total.exists():
            return total.aggregate(avg_rate=Avg("rating"))["avg_rate"]
    return "N/A"