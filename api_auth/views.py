from .serializers import UserSerializerCreated, PasswordResetSerializer, UserSerializerList
from .send_email import send_email
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import re
from rest_framework import generics
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated 


class UserRegistrationAPI(generics.CreateAPIView):
    """
    An endpoint for created new user.
    """
    serializer_class = UserSerializerCreated


class UserListAPI(generics.ListAPIView):
    """
    An endpoint for list users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializerList


class UserDetailAPI(generics.RetrieveUpdateAPIView):
    """
    An endpoint for datail user.
    """
    serializer_class = UserSerializerList
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class UserUpdateAPI(APIView):
    """
    An endpoint for update user.
    """
    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        print(user)
        serializer = UserSerializerList(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Old password invalid"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    """
     An endpoint to change the password via email.
    """
    serializer_class = PasswordResetSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['email']).first()
            if user:
                send_email(user=user)
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password reset sent by email',
                    'data': []
                    }
                return Response(data=response)
            else:
                return Response(data={"Error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializer.errors)


def password_account(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.filter(pk=uid)

    user_is_valid = (user := user.first()) and default_token_generator.check_token(user, token)

    if request.method == 'GET':
        if user_is_valid:
            return render(request, 'mail/reset_confirm.html')  

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
        if user_is_valid:
            user.set_password(password)
            user.save()
            return HttpResponse({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'successfully changed password',
                    'data': []
                    })
