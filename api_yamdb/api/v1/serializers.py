from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = '__all__'


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
    year = serializers.IntegerField()

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

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context[
                'request'
            ].parser_context['kwargs']['title_id']
            if Review.objects.filter(author=self.context['request'].user,
                                     title_id=title_id).exists():
                raise serializers.ValidationError('Публиковать более одного'
                                                  ' обзора на одно и то же'
                                                  ' произведение нельзя!')
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
