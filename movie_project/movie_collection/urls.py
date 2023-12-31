from django.urls import path
from .views import SignUpAPI, CollectionViewSet, MovieViewSet, MoviesView, RequestCounterView

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('collections/', CollectionViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='collection-list'),
    path('collections/<uuid:pk>/', CollectionViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='collection-detail'),
    path('movies/',
         MovieViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie-list'),
    path('movies/<uuid:pk>/', MovieViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='movie-detail'),
    path('get-top-genres/', MoviesView.as_view(), name='get-top-genres'),
    path('request-count/', RequestCounterView, name='request-count'),
    path('request-count/reset/', RequestCounterView, name='reset-request-count'),
]
