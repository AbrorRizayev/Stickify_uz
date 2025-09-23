from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import (CharField, EmailField, Form, ModelForm,
                          PasswordInput, TextInput)
from jsonschema import ValidationError

from .models import Category, Product, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "fullname", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "fullname", "phone_number", "subscription_end")


class LoginForm(Form):
    email = EmailField(label="Email")
    password = CharField(label="Password", widget=PasswordInput)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "color", "size", "brand", "material", "article", "manufacture",
                  "region", "city", "street_and_home", "barcode"]
        widgets = {
            "barcode": TextInput(attrs={"style": "font-family: 'Courier New', monospace;"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        barcode = cleaned_data.get("barcode")

        if self.user and name and barcode:
            exists = Product.objects.filter(
                user=self.user,
                name=name,
                barcode=barcode
            ).exists()
            if exists:
                raise forms.ValidationError(
                    "❌ Siz bu mahsulotni allaqachon qo‘shgansiz!"
                )
        return cleaned_data


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if self.user and Category.objects.filter(user=self.user, name=name).exists():
            raise ValidationError("Bu nomdagi kategoriya allaqachon mavjud!")
        return name
