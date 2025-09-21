import uuid

from django.db.models import Model, FileField, ForeignKey, CASCADE, TextChoices, UUIDField
from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, DateTimeField
from django.utils import timezone
from root.settings import AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = EmailField(max_length=255, unique=True)
    fullname = CharField(max_length=255)
    phone_number = CharField(max_length=15, unique=True, null=True, blank=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    subscription_end = DateTimeField(null=True, blank=True)

    def activate_subscription(self, period: str = "1m"):
        now = timezone.now()

        if period == "15m":
            delta = timedelta(minutes=15)
        elif period == "1m":
            delta = timedelta(days=30)
        elif period == "3m":
            delta = timedelta(days=90)
        elif period == "6m":
            delta = timedelta(days=180)
        elif period == "1y":
            delta = timedelta(days=365)
        else:
            raise ValueError("Invalid subscription period")

        if self.subscription_end and self.subscription_end > now:
            self.subscription_end += delta
        else:
            self.subscription_end = now + delta

        self.is_active = True
        self.save()

    def check_subscription(self):
        if self.subscription_end and self.subscription_end < timezone.now():
            return False
        return True


class Category(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(AUTH_USER_MODEL, CASCADE, related_name="categories")
    created_at = DateTimeField(auto_now_add=True)
    name = CharField(max_length=255)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return self.name



class Product(Model):
    class StickerType(TextChoices):
        SMALL = '58X40mm', "58X40mm"
        MEDIUM = '70X40mm', "70X40mm"
        LARGE = '100X50mm', "100X50mm"

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(AUTH_USER_MODEL, CASCADE, related_name="products")
    category = ForeignKey(Category, CASCADE, related_name="products")
    # color = ForeignKey(ColorOfSticker, on_delete=CASCADE, related_name="products")

    name = CharField(max_length=255)
    size = CharField(max_length=255)
    type = CharField(max_length=20, choices=StickerType.choices)
    brand = CharField(max_length=255)
    color = CharField(max_length=255)
    material = CharField(max_length=255)
    article = CharField(max_length=255)
    manufacture = CharField(max_length=255)
    region = CharField(max_length=255)
    city = CharField(max_length=255)
    street_and_home = CharField(max_length=255)
    barcode = CharField(max_length=255)

    def __str__(self):
        return f"{self.name})"