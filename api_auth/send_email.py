from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


def generate_url(user: User):
    protocol = 'http' if settings.DEBUG else 'https'
    domain = settings.DOMAIN
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uid64': uid, 'token': token})}"  # noqa: E501
    return url


def send_email(user: User):
    url = generate_url(user=user)
    subject = "Reset password"
    mail_body = render_to_string('mail/reset_password.html', {'url': url})
    email = EmailMessage(subject, mail_body, to=[user.email])
    if email.send():
        # TODO: add log success
        pass
    else:
        # TODO: add log error
        pass
