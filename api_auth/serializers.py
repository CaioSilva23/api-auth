# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .utils import strong_password


# class UsuarioSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(validators=[strong_password],)

#     class Meta:
#         model = User
#         fields = ('username','email', 'password')

#     def create(self, validated_data):
#         user = super().create(validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
        
#         return user
    
#     password2 = serializers.SerializerMethodField(
#         method_name='password2',

#     )

#     def password2(self, password2):
#         print(password2)


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
        fields = ['username','first_name', 'last_name', 'email', 'password', 'password2']
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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
    re_new_password = serializers.CharField(max_length=128)