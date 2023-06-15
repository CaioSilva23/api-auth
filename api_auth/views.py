from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView, PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.template.loader import get_template
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserCreateView(generics.CreateAPIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetView(APIView):
    def _generate_url(self, user: User):
        protocol = 'http' if settings.DEBUG else 'https'
        domain = settings.DOMAIN
        uid = urlsafe_base64_encode(force_bytes(user.pk))#  CODIFICA O ID DO USUÁRIO noqa: E501
        token = default_token_generator.make_token(user) #  GERA O TOKEN A PARTIR DO USER

        url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uid64': uid, 'token': token})}"
        
        return url

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    resert_password_url = self._generate_url(user=user)
                    subject = "Ative sua conta na EDIV..."
                    mail_body = render_to_string('mail/reset_password.html', {'url': resert_password_url})
                    email = EmailMessage(subject, mail_body, to=[user.email])
                    if email.send():
                        # TODO: add log success
                        pass
                    else:
                        # TODO: add log error
                        pass
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .utils import strong_password
import re
from django.shortcuts import redirect

def password_account(request, uid64, token):
    if request.method == 'GET':
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.filter(pk=uid)
        if (user := user.first()) and default_token_generator.check_token(user, token):
            return render(request, 'reset.html')
    
    elif request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        url = redirect(reverse('password_reset_confirm', kwargs={'uid64': uid64, 'token': token}))

  
        if password != password2:
            messages.error(request, 'As senhas não se coincidem!')
            return url

        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
        if not regex.match(password):
            messages.error(request, 'No mínimo 8 caracteres, '
            'possuir pelo menos uma letra minuscula, '
            'uma letra maiúscula e um número')
            return url
        return HttpResponse('Senha válida')