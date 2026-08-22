from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer

# Create your views here.

class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':f'User created with username: {request.data.get('username')}'}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key})
        return Response({'error':'Invalid username or password!'})


class LogoutAPIView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response({'message':'Logged out successfully!'})

