from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm
)
from django.utils.translation import gettext_lazy as _

from recipes_app.models import DishRating


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control input-sm",
                "placeholder": "username",
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
            }
        ),
    )


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[("zero", 0), ("one", 1), ("Two", 2), ("Three", 3), ("Four", 4), ("Five", 5)],
        widget=forms.Select(
            attrs={
                "class": "rating-section"
            }
        )
    )
    class Meta:
        model = DishRating
        fields = ["rating"]