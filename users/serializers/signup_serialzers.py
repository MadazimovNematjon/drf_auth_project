from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import random
from shared.utils import validate_email_or_username, send_email
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id',
                  'auth_status',
                  )

        extra_kwargs = {
            'auth_status': {'read_only': True, 'required': False},
        }

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        #   email send code
        code = user.create_verify_code()
        print("created code {}".format(code))
        # send_email(receiver_mail=user.email,code=code)

        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email')).lower()
        input_type = validate_email_or_username(user_input)

        if input_type == 'email':
            data['email'] = user_input
        else:
            data = {
                'success': False,
                'message': 'Invalid input type.',
            }
            raise ValidationError(data)
        print(f"user_input: {data}")
        print(f"user_input: {input_type}")

        return data

    def validate_email_phone(self, value):
        value = value.lower()
        if value and User.objects.filter(email=value).exists():
            data = {
                'success': False,
                'message': 'Email already exists.',
            }
            raise ValidationError(data)
        return value

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.tokens())
        return data
