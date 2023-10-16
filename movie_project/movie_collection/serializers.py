from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db.models.query import Prefetch
import os


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data['password'].strip()
        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['uuid', 'title', 'description', 'genres']


class CollectionSerializer(serializers.ModelSerializer):

    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            Movie.objects.create(collection=collection, **movie_data)
        return collection


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"


class RequestCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCount
        fields = "__all__"
