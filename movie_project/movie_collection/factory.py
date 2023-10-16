import factory
from .models import Collection, Movie

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Sequence(lambda n: f'Test Collection {n}')
    description = "Test description"

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Sequence(lambda n: f'Test Movie {n}')
    description = "Test movie description"
    genres = "Action"