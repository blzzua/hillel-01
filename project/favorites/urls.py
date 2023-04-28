from django.urls import path
from favorites.views import AddToFavorites

urlpatterns = [
    path('add', AddToFavorites.as_view(), name='favorite_add'),
]
