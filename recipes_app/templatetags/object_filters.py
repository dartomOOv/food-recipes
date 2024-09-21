from django import template
from django.db.models import Avg

from recipes_app.models import SavedUserDish, DishRating

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
def average_rating(dish):
    avg_rate = DishRating.objects.filter(dish=dish)
    if avg_rate.exists():
        return avg_rate.aggregate(avg_rate=Avg("rating"))["avg_rate"]
    return "N/A"


@register.filter
def dish_rated(dish, user):
    filtered = DishRating.objects.filter(dish=dish, user=user)
    return filtered.exists()