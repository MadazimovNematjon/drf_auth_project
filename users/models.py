import uuid
import random

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
import datetime
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel

ORDINARY_USER, ADMIN, MANAGER = ("ordinary_user", "admin", "manager")
NEW, CODE_VERIFIER, SIGNUP, PHOTO_DONE, DONE = ('new', 'code', 'signup', 'photo-done', 'done')


class User(AbstractUser, BaseModel):
    USER_ROLE = (
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER)
    )

    AUTH_STATUS_CHOICES = (
        (NEW, NEW),
        (CODE_VERIFIER, CODE_VERIFIER),
        (SIGNUP, SIGNUP),
        (PHOTO_DONE, PHOTO_DONE),
        (DONE, DONE),
    )

    user_role = models.CharField(max_length=25, choices=USER_ROLE, default=ORDINARY_USER)
    auth_status = models.CharField(max_length=25, choices=AUTH_STATUS_CHOICES, default=NEW)
    email = models.EmailField(unique=True, null=True, blank=True)
    photo = models.ImageField(
        upload_to='media/user_photo/',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]  # Example extensions
    )

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}'  # instagram-23324fsdf
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{str(random.randint(0, 9))}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f"password-{str(uuid.uuid4().__str__().split('-')[-1])}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)


CODE_EXPIRE = 2


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    user = models.ForeignKey('users.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        self.expiration_tim = datetime.datetime.now() + datetime.timedelta(minutes=CODE_EXPIRE)

        super(UserConfirmation, self).save(*args, **kwargs)
