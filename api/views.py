from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Todo
from .serializers import TodoSerializer

# Create your views here.


class TodoListCreateAPIView(ListCreateAPIView):
    # queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class RootAPIView(APIView):
    def get(self, request):
        return Response({'todos':reverse('todos', request=request)})
