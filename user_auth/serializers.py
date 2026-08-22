from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
