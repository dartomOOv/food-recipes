from django import template

from recipes_app.models import SavedUserDish

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
