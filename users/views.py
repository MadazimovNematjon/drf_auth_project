from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .models import User
from users.serializers.signup_serialzers import SignUpSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
