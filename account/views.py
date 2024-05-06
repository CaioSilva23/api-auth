from rest_framework.response import Response
from rest_framework import status
from account.serializers import UserRegistrationSerializer,\
                                UserLoginSerializer, \
                                UserProfileSerializer, \
                                UserChangePasswordSerializer, \
                                SendPasswordResetEmailSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView
from account.models import User


# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


class UserRegistrationAPI(CreateAPIView):
    """
    An endpoint for register user.
    """
    renderer_classes = [UserRenderer]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user=user)
        return Response(
                data={'token': token, 'mgs': 'Registration Success'},
                status=status.HTTP_201_CREATED)


class UserLoginAPI(GenericAPIView):
    """
    An endpoint for login user.
    """
    renderer_classes = [UserRenderer]
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email', "")
        password = serializer.data.get('password', "")

        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user=user)
            return Response({'token': token, 'success': 'Login success'}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'error': 'Email or Password is not valid'},
                status=status.HTTP_404_NOT_FOUND)


class UserProfileAPI(GenericAPIView):
    """
    An endpoint for profile user.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, format=None):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(GenericAPIView):
    """
    An endpoint for change password.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def put(self, request, format=None):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})  # noqa: E501
        serializer.is_valid(raise_exception=True)
        return Response(
                data={'msg': 'Password Changed Successfully'},
                status=status.HTTP_200_OK)


class PasswordResetEmailView(GenericAPIView):
    """
     An endpoint to change the password via email.
    """
    renderer_classes = [UserRenderer]
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
                data={'success': 'New password has been sent to your email'},
                status=status.HTTP_200_OK)
