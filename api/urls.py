from django.urls import path
from . import views

urlpatterns = [
    path('', views.RootAPIView.as_view(), name='root'),
    path('todos/', views.TodoListCreateAPIView.as_view(), name='todos'),
    path('todo/<int:pk>/', views.TodoRetrieveUpdateDestroyAPIView.as_view(), name='todo'),
]
