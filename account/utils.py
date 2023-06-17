import re
from rest_framework import serializers
from django.core.mail import EmailMessage
import os


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
    @staticmethod
    def send_email(data):
        email = EmailMessage(
                subject=data['subject'],
                body=data['body'],
                from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                to=[data['to_email']]
                )
        email.send()
