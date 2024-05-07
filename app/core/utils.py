import re, os, random, string

from rest_framework import serializers

from core.models import User

from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise serializers.ValidationError((
            'No mínimo 8 caracteres, '
            'possuir pelo menos uma letra minuscula, '
            'uma letra maiúscula e um número'
        ),
            code='invalid')


# VALIDADOR DE CPF
def cpf_validate(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


class Util:
    @classmethod
    def send_email(cls, user: User, new_password: string) -> None:
        try:
            body = 'New Password ' + new_password
            email = EmailMessage(
                    subject='Reset Your Password',
                    body=body,
                    from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                    to=[user.email]
                    )
            email.send()
        except Exception:
            raise serializers.ValidationError((
                'Internal Error'
            ),
                code='invalid')
        return True


    @classmethod
    def generate_url(cls, user: User):
        # protocol = 'http' if settings.DEBUG else 'https'
        domain = settings.DOMAIN
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        url = f"{domain}{reverse('reset-password', kwargs={'uid': uid, 'token': token})}"  # noqa: E501
        return url

    @classmethod
    def generate_temp_password(cls):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(8))
