from django.contrib import admin

from recipes_app.models import Dish, Ingredient, Category, DishType, IngredientAmount


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "get_ingredients"]

    def get_ingredients(self, obj):
        products_list = [
            f"{ingredient.ingredient.name}: {ingredient.amount}"
            for ingredient in obj.ingredients.all()
        ]
        return "; ".join(products_list)


# admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(DishType)
admin.site.register(IngredientAmount)
