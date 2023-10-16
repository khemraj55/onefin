from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .factory import CollectionFactory, MovieFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
import uuid

class TestViews(APITestCase):
    
    def setUp(self):
        self.collection = CollectionFactory()

    def test_signup_api(self):
        url = '/api/signup/'
        data = {'username': 'testuser',
                'password': 'testpassword', 'email': 'email@gmail.com'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_fields = ['username', 'email']
        for field in expected_fields:
            self.assertIn(field, response.data)

    
    def test_create_collection(self):
        movie = MovieFactory()
        data = {'title': 'Test Collection', 'movies': [
            {'title': movie.title, 'description': movie.description, 'genres': movie.genres}]}
        url = '/api/collections/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_fields = ['title', 'description', 'movies']
        for field in expected_fields:
            self.assertIn(field, response.data)
            
    def test_collection_detail(self):
        """Test collection detail view"""

        # Access the collection detail view
        url = f'/api/collections/{self.collection.uuid}/'
        response = self.client.get(url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the expected fields
        expected_fields = ['title', 'description', 'movies']
        for field in expected_fields:
            self.assertIn(field, response.data)

class TestMovies(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def test_movie_creation(self):
        self.client.force_authenticate(user=self.user)
        movie = Movie.objects.create(
            title="Test Movie", description="This is a test movie", genres="Test")

        url = '/api/movies/'
        data = {'title': movie.title,
                'description': movie.description, 'genres': movie.genres}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_fields = ['title', 'description', 'genres']
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_movie_retrieval(self):

        movie = Movie.objects.create(
            title="Test Movie", description="This is a test movie", genres="Test")
        url = f'/api/movies/{movie.uuid}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = ['title', 'description', 'genres']
        for field in expected_fields:
            self.assertIn(field, response.data)
