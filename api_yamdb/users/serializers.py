from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from users.exeptions import InvalidConfirmationCode, NoneConfirmationCode
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    forbidden_usernames = ('me', 'admin', 'superuser')
    default_error_messages = {
        'forbidden_username': 'Username `{name}` is forbidden.',
        'uniq_email': 'User with email `{email}` already exists.',
    }

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                self.error_messages['uniq_email'].format(email=value),
                code='uniq_email',
            )
        return value

    def validate_username(self, value):
        if value in self.forbidden_usernames:
            raise serializers.ValidationError(
                self.error_messages['forbidden_username'].format(name=value),
                code='forbidden_username',
            )
        return value


class SelfUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        extra_kwargs = {
            'email': {'required': True},
            'role': {'read_only': True},
        }


class ConfirmationCodeTokenSerializer(serializers.Serializer):
    username = serializers.SlugField()
    confirmation_code = serializers.IntegerField()
    token_class = AccessToken
    default_error_messages = {
        'no_active_account': (
            'No active account found with the given credentials'
        ),
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            'request': self.context.get('request'),
            'username': attrs['username'],
            'confirmation_code': attrs['confirmation_code'],
        }

        try:
            self.user = authenticate(**authenticate_kwargs)
        except User.DoesNotExist:
            raise exceptions.NotFound()
        except NoneConfirmationCode as e:
            raise exceptions.APIException(e.message)
        except InvalidConfirmationCode as e:
            raise exceptions.ValidationError(e.message)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        token = self.get_token(self.user)
        return {'token': str(token)}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
