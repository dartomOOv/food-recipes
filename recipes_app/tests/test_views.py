from django.test import TestCase, Client
from django.urls import reverse

from recipes_app.models import (
    User,
    Category,
    Dish,
    DishType,
    Ingredient,
    IngredientAmount,
)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            first_name="firsttest",
            last_name="lasttest",
            username="usernametest",
            email="test@test.com",
            password="passwordtest",
        )
        self.category = Category.objects.create(name="categorytest")
        self.ingredient = Ingredient.objects.create(name="ingredienttest", category=self.category)
        self.ingr_amount = IngredientAmount.objects.create(ingredient=self.ingredient, amount="testamount")
        self.dish_type = DishType.objects.create(name="testtype")
        times = 10
        for time in range(1, times + 1):
            dish = Dish.objects.create(
                name=f"test{time}name",
                description=f"test{time}description",
                dish_type=self.dish_type,
                cooking_time=times,
                how_to_cook=f"test{time}how_to_cook",
                created_by=self.user
            )
            dish.ingredients.add(self.ingr_amount)
        self.client.force_login(self.user)

    def test_search_form_result(self):
        res = reverse("recipes:recipes-list")
        url = f"{res}?name=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object_list"].count(), 1)
        self.assertTrue(Dish.objects.get(id=2) in response.context["object_list"])

    def test_if_paginated_by_six(self):
        response = self.client.get(reverse(f"recipes:recipes-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["object_list"]), 6)
