from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Product, User

User = get_user_model()


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('user',)


class StickerSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    gs1_code = serializers.CharField(max_length=150, min_length=50)

# -========================== User Serializers ============================
class UserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("This email is already registered.Go Login in!")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError({'Confirm Password': "Passwords do not match."})
        attrs.pop('confirm_password', None)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'   # 👈 email orqali login

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)
        if user is None:
            raise serializers.ValidationError("Email yoki parol noto‘g‘ri.")

        data = super().validate(attrs)
        return data



class ConfirmRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ListUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'email',


class StickerCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
