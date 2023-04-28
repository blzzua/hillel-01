from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import FormView

from favorites.models import FavoriteItem
from favorites.forms import AddToFavoritesForm
from django.http import HttpResponseNotAllowed, HttpResponse

User = get_user_model()

# Create your views here.

class AddToFavorites(FormView):
    model = FavoriteItem
    form_class = AddToFavoritesForm
    def post(self, request):
        form = AddToFavoritesForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            user = request.user
            favorite_item, action = FavoriteItem.objects.get_or_create(user_id=user, item_id=item_id)
            if action:
                return HttpResponse(f'Item added', 200)
            else:
                return HttpResponse(f'Item already added', 200)
        else:
            return HttpResponse('Bad Request', status=400)

    def get(self, request):
        return HttpResponseNotAllowed('GET prohibited')
