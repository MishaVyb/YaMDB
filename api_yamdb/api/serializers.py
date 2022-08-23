import datetime
from django.core.validators import MaxValueValidator
from rest_framework import serializers

from reviews.models import Title, Genre, Category


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
