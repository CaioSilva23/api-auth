from rest_framework import serializers
from django.contrib.auth.models import User
from .utils import strong_password


class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[strong_password],)

    class Meta:
        model = User
        fields = ('username','email', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    
    password2 = serializers.SerializerMethodField(
        method_name='password2',

    )

    def password2(self, password2):
        print(password2)
