from django.contrib import admin

# Register your models here.
from .models import *

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('uuid','title','description',)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'genres', 'uuid')


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Movie, MovieAdmin)