from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from recipes_app.models import DishRating, Dish


class CustomRegisterForm(UserCreationForm):
    username = UsernameField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-sm",
                "placeholder": "Your username",
            }
        ),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-sm",
                "placeholder": "Your first name",
            }
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-sm",
                "placeholder": "Your last name",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control input-sm",
                "placeholder": "Your email",
            }
        ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control input-sm",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control input-sm",
                "placeholder": "Confirm password",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control input-sm",
                "placeholder": "username",
                "value": "test_username"
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control input-sm",
                "placeholder": "password",
                "value": "s0me_paSSw0rd"
            }
        ),
    )


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        widget=forms.Select(
            attrs={"class": "rating-section"}
        ),
    )

    class Meta:
        model = DishRating
        fields = ["rating"]


class DishCreateForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            "description",
            "dish_type",
            "cooking_time",
            "ingredients",
            "how_to_cook",
        ]
        widgets = {"ingredients": forms.CheckboxSelectMultiple}


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "form-control",
            }
        ),
    )
