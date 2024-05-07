"""
Serializer for user.
"""

from rest_framework import serializers
from core.models import User
from core.utils import strong_password, Util
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError  # noqa: E501
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User serializer registration"""
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
            }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        strong_password(password)
        return attrs

    def create(self, validate_data):
        del validate_data['password2']
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """User serializer login"""
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    """User serializer profile"""
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    """User serializer chance password"""
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['old_password', 'new_password', 'new_password2']

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')

        user = self.context.get('user')

        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password")

        if new_password != new_password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")

        strong_password(new_password)

        user.set_password(new_password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    """User serializer reset password"""
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email)

        if user.exists():
            user = user.first()
            temp = Util.generate_temp_password()
            success = Util.send_email(
                user=user,
                new_password=temp)

            if success is True:
                user.set_password(temp)
                user.save()
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')
