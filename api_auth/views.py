from .serializers import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserCreated(APIView):
    def post(self, request, format=None):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"Success": "Usuário cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)