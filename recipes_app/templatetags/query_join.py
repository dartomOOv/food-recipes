from django import template

register = template.Library()

@register.filter
def join_authors(user_dishes):
    return ", ".join(
        [user_dish.user.username for user_dish in user_dishes.all().select_related("user")]
    )