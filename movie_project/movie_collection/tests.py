from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .factory import CollectionFactory, MovieFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
import uuid
import unittest

class TestViews(APITestCase):

    def setUp(self):
        self.collection = CollectionFactory()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    

    def test_create_collection(self):
        movie = MovieFactory()
        movies_data = [
            {'title': movie.title, 'description': movie.description, 'genres': movie.genres}
        ]
        url = '/api/collections/'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {'title': 'Test Collection', 'movies': movies_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_fields = ['title', 'description', 'movies', 'uuid']
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_collection_detail(self):
        url = f'/api/collections/{self.collection.uuid}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = ['uuid','title', 'description', 'movies']
        for field in expected_fields:
            self.assertIn(field, response.data)

class TestMovies(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_movie_creation(self):
        self.client.force_authenticate(user=self.user)
        movie = MovieFactory()
        url = '/api/movies/'
        data = {'title': movie.title,
                'description': movie.description, 'genres': movie.genres}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_fields = ['title', 'description', 'genres']
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_movie_retrieval(self):
        movie = MovieFactory()
        url = f'/api/movies/{movie.uuid}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = ['title', 'description', 'genres']
        for field in expected_fields:
            self.assertIn(field, response.data)