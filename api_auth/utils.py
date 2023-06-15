import re
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'No mínimo 8 caracteres, '
            'possuir pelo menos uma letra minuscula, '
            'uma letra maiúscula e um número'
        ),
            code='invalid'
        )
