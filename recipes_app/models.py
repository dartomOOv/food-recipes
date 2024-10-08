from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

from config.settings import AUTH_USER_MODEL


class User(AbstractUser):

    def __str__(self):
        return f"{self.username} ({self.first_name}, {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    dish_type = models.ForeignKey(to="DishType", related_name="dishes", on_delete=models.CASCADE)
    cooking_time = models.CharField(max_length=64)
    ingredients = models.ManyToManyField(to="Ingredient", related_name="ingredient_dishes")
    how_to_cook = models.TextField(max_length=2048)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "dishes"
        db_table = "dish"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.description} (type: {self.dish_type.name}, rating: {self.user_rates.aggregate(Avg('self__value'))})"


class Ingredient(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        db_table = "ingredient"


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"


class DishType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dish_type"

class DishRating(models.Model):
    dish = models.ForeignKey(to="Dish", on_delete=models.CASCADE, related_name="user_rates")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rated_dishes")
    rating = models.FloatField(null=True)

    class Meta:
        unique_together = ["dish", "user"]
        db_table = "dish_rating"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=0) & models.Q(rating__lte=5),
                name="rating_limits")
        ]


class DishLike(models.Model):
    dish = models.ForeignKey(to="Dish", on_delete=models.CASCADE, related_name="user_likes")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_dishes")

    class Meta:
        unique_together = ["dish", "user"]
        db_table = "dish_like"


class CreatedUserDish(models.Model):
    dish = models.ForeignKey(to="Dish", on_delete=models.CASCADE, related_name="user_dishes")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_dishes")

    class Meta:
        unique_together = ["dish", "user"]
        db_table = "created_user_dish"


class SavedUserDish(models.Model):
    dish = models.ForeignKey(to="Dish", on_delete=models.CASCADE, related_name="user_saves")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_dishes")

    class Meta:
        unique_together = ["dish", "user"]
        db_table = "saved_user_dish"
