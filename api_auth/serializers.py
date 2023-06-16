from rest_framework import serializers
from django.contrib.auth.models import User
from .utils import strong_password
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserSerializer(serializers.ModelSerializer):
    username_validator = UnicodeUsernameValidator()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(validators=[strong_password])

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("As senhas não coincidem.")
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Usuário com este email já existe!")
        # strong_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# SERIALIZER EMAIL RECOVER PASSWORD
class PasswordResetSerializer(serializers.Serializer):
    model = User
    email = serializers.EmailField()


# SERIALIZER RESET PASSWORD OLD
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)