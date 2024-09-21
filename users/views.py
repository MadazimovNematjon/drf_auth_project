from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import User, DONE, CODE_VERIFIER, NEW
from users.serializers.signup_serialzers import SignUpSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class VerifyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
        code = request.data.get('code',None)

        self.check_verify(user=user, code=code)
        data = {
            'success': True,
            'auth_status': user.auth_status,
            'access_token': user.tokens()['access_token'],
            'refresh_token': user.tokens()['refresh_token'],
            'message': 'Verified',
        }
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        print(f"verifies: {verifies}")
        if not verifies.exists():
            data = {
                'success': False,
                'message': 'Sizning kodingiz eskirgan yoki xato',
            }
            raise ValidationError(data)
        else:

            verifies.update(is_confirmed=True)

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIER
            user.save()
        return True
