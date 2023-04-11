# from django.http import HttpResponse
from django.shortcuts import render, redirect

from items.forms import ItemCreateForm
from items.models import Item
from django.contrib import messages
from django.views.generic import ListView, View, TemplateView
from django.core.paginator import Paginator


class ItemsListView(ListView):
    model = Item
    paginate_by = 5
    paginator = Paginator
    template_name = 'items/list.html'


class ItemCreateView(View):
    def get(self, request):
        form = ItemCreateForm()
        context = {'form': form}
        return render(request, 'items/item_create.html', context)

    def post(self, request):
        form = ItemCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item has been created successfully')
            return redirect('items_list')
        else:
            messages.error(request, 'Error creating item')
            context = {'form': form}
            return render(request, 'items/item_create.html', context=context)

class MainPage(TemplateView):
    template_name = "index.html"
