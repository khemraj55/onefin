
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import Counter
from rest_framework.decorators import action
from .middleware import RequestCounterMiddleware
from .models import Collection, Movie
from .serializers import CollectionSerializer, MovieSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
request_counter_middleware = RequestCounterMiddleware(None)


class MoviePagination(PageNumberPagination):
    page_size = 10


class SignUpAPI(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class CollectionViewSet(viewsets.ModelViewSet):
    # queryset = Collection.objects.all()
    # serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def create(self, request, *args, **kwargs):

        movies_data = request.data.pop('movies')

        # Create the collection
        collection_serializer = self.get_serializer(data=request.data)
        if collection_serializer.is_valid():
            collection = collection_serializer.save()

            # Create associated movies
            movie_serializer = MovieSerializer(data=movies_data, many=True)
            if movie_serializer.is_valid():
                for movie_data in movies_data:
                    Movie.objects.create(collection=collection, **movie_data)
                return Response(collection_serializer.data, status=status.HTTP_201_CREATED)
            else:
                collection.delete()
                return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(collection_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_movies(self, request, pk=None):
        collection = self.get_object()
        serializer = self.get_serializer(collection, data=request.data, partial=True, validate_movies=self.validate_movies)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'collection_uuid': collection.uuid})

    def collection_detail(self, request, pk):
        try:
            collection = get_object_or_404(Collection, pk=pk)
            movies = Movie.objects.filter(collection=collection)
            movies_serializer = MovieSerializer(movies, many=True)

            response_data = {
                'collection': CollectionSerializer(collection).data,
                'movies': movies_serializer.data
            }
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.get_serializer(data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)

    #         movies = request.data.pop('movies', [])

    #         collection = serializer.save()

    #         for movie_data in movies:
    #             Movie.objects.create(collection=collection, **movie_data)

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

    def perform_create(self, serializer):
        serializer.save()


class MoviesView(APIView):
    def get(self, request):
        try:
            movies = Movie.objects.all()
            paginator = MoviePagination()
            page = paginator.paginate_queryset(movies, request)
            serializer = MovieSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=False)
    def get_top_genres(self, request):
        try:
            movies = Movie.objects.filter(collection=request.user.collection)
            genres = movies.values_list("genres", flat=True)
            genres = [genre for genre in genres if genre]
            genres = Counter(genres).most_common(3)
            return Response([genre[0] for genre in genres])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RequestCounterView(View):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self):
        try:
            return JsonResponse({'requests': request_counter_middleware.get_request_count()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            request_counter_middleware.reset_request_count()
            return JsonResponse({'message': 'request count reset successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

