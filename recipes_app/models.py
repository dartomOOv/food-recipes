from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from config.settings import AUTH_USER_MODEL

class User(AbstractUser):
    slug = AutoSlugField(populate_from=["date_joined__second", "username", "date_joined__microsecond"])

    def __str__(self):
        return f"{self.username} ({self.first_name}, {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    dish_type = models.ForeignKey(to="DishType", related_name="dishes", on_delete=models.CASCADE)
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(to="IngredientAmount", related_name="dishes")
    how_to_cook = models.TextField(max_length=4096)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=AUTH_USER_MODEL, related_name="dishes", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=["name", "created_at__microsecond"])

    class Meta:
        verbose_name_plural = "dishes"
        db_table = "dish"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cooking_time__gte=0),
                name="cooking_time_limit")
        ]

    def get_absolute_url(self):
        return reverse('recipes:recipe-detail', kwargs={'slug': self.slug})


    def __str__(self):
        return f"""
            {self.name} - {self.description} 
            (type: {self.dish_type.name})
        """


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(to="Ingredient", on_delete=models.CASCADE, related_name="amounts")
    amount = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.ingredient}, {self.amount}"

    class Meta:
        db_table = "ingredient_amount"
        unique_together = ["ingredient", "amount"]


class Ingredient(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        unique_together = ["name", "category"]
        db_table = "ingredient"


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"


class DishType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dish_type"


class DishRating(models.Model):
    dish = models.ForeignKey(to="Dish", on_delete=models.CASCADE, related_name="user_rates")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rated_dishes")
    rating = models.IntegerField(null=True)

    class Meta:
        unique_together = ["dish", "user"]
        db_table = "dish_rating"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=0) & models.Q(rating__lte=5),
                name="rating_limits")
        ]


class SavedUserDish(models.Model):
    dish = models.ForeignKey(to="Dish", on_delete=models.CASCADE, related_name="user_saves")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_dishes")

    class Meta:
        db_table = "saved_user_dish"
