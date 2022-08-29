from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.exeptions import InvalidConfirmationCode, NoneConfirmationCode
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug'
    )
    year = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'category', 'genre', 'year')


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context['request'].parser_context['kwargs'][
                'title_id'
            ]
            if Review.objects.filter(
                author=self.context['request'].user, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Публиковать более одного'
                    ' обзора на одно и то же'
                    ' произведение нельзя!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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
        except NoneConfirmationCode as exception:
            raise exceptions.APIException(exception.message)
        except InvalidConfirmationCode as exception:
            raise exceptions.ValidationError(exception.message)

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
