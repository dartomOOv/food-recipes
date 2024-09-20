from django import template

from recipes_app.models import SavedUserDish

register = template.Library()

@register.filter
def dish_is_saved(dish, user):
    filtered = SavedUserDish.objects.filter(dish=dish, user=user)
    return filtered.exists()