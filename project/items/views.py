# from django.http import HttpResponse
from django.shortcuts import render

from items.forms import ItemsForm
from items.models import Item


# Create your views here.
def indexfail(request):
    return render(request, 'index.html', context={})


def index(request, *args, **kwargs):
    products_list = Item.objects.all()
    if request.method == 'POST':
        form = ItemsForm(data=request, files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ItemsForm()
    return render(request, 'products_index.html', context={'product': products_list,  'form': form})
