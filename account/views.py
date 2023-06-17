from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,\
                                UserLoginSerializer, \
                                UserProfileSerializer, \
                                UserChangePasswordSerializer, \
                                SendPasswordResetEmailSerializer, \
                                UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationAPI(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user=user)
        return Response(
                data={'token': token, 'mgs': 'Registration Success'},
                status=status.HTTP_201_CREATED)


class UserLoginAPI(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user=user)
            return Response({'token': token, 'msg': 'Login success'}, status=status.HTTP_200_OK)  # noqa: E501
        else:
            return Response(
                data={'erros': {'non_field_errors': ['Email or Password is not valid']}},  # noqa: E501
                status=status.HTTP_404_NOT_FOUND)


class UserProfileAPI(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
                        data=request.data,
                        context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response(
                data={'msg': 'Password Changed Successfully'},
                status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
                data={'msg': 'Password Reset link send. Please check your Email'},  # noqa: E501
                status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
                                        data=request.data,
                                        context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(
                    data={'msg': 'Password Reset Successfully'},
                    status=status.HTTP_200_OK)
