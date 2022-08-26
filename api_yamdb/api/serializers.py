import datetime
from django.core.validators import MaxValueValidator
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from reviews.models import Title, Genre, Category
from users.models import User
from reviews.models import Review, Comment

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(
        validators=[MaxValueValidator(datetime.date.today().year)]
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'category',
                  'genre', 'year')



class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def create(self, validated_data):
        request = self.context.get('request')
        title_id = self.context.get('title_id')
        author = request.user
        try:
            obj = Review.objects.create(
                text = validated_data['text'],
                author = author,
                score = validated_data['score']
                title = self.context.get('title')
            )
        except ValidationError as ex:
            raise serializers.ValidationError({'detail': "It's impossible to create"})
        return obj


    def validate_score(self, value):
        if not 1 <= int(value) <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
