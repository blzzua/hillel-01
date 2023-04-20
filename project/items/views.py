# from django.http import HttpResponse
import csv
import logging
import contextlib

from django.shortcuts import render, redirect
from django.http import HttpResponse
from items.forms import ItemCreateForm, ImportItemsCSVForm
from items.models import Item
from django.contrib import messages
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.db import DatabaseError, transaction


class ItemsListView(ListView):
    model = Item
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


class MainPage(ItemsListView):
    paginate_by = 8
    paginator = Paginator
    template_name = 'products_index.html'


class ImportItemsListView(View):

    def get(self, request, *args, **kwargs):
        form = ImportItemsCSVForm()
        saved_items = []
        return render(request, 'items/import_csv.html', {'form': form, 'saved_items': saved_items})

    def post(self, request, *args):
        form = ImportItemsCSVForm(request.POST, request.FILES)
        if form.is_valid():
            logging.warning(f'form is valid')
            csv_file = request.FILES['csv_file']
            # TODO implement single-transaction .
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            dict_reader = csv.DictReader(decoded_file)
            errors = []
            on_duplicate = form.cleaned_data['on_duplicate']
            saved_items = []
            ctx_mgr = transaction.atomic() if form.cleaned_data['single_transaction'] else contextlib.nullcontext()
            for row in dict_reader:
                if Item.objects.filter(caption=row['caption']).exists():
                    logging.error(f'update {row["caption"]} with {on_duplicate=}')
                    if on_duplicate == 'update':
                        # item = Item.objects.filter(caption=row['caption']).first()
                        item_qs = Item.objects.filter(caption=row['caption'])
                        item_qs.update(
                            caption=row['caption'], sku=row['sku'], price=row['price'],
                            is_active=row['is_active'], description=row['description']
                        )
                        item = Item.objects.filter(caption=row['caption']).first()
                        errors.append(item)
                    elif on_duplicate == 'ignore':
                        pass
                else:
                    logging.warning(f'insert {row["caption"]} with {on_duplicate=}')
                    try:
                        item = Item.objects.create(caption=row['caption'], sku=row['sku'], price=row['price'],
                                               is_active=row['is_active'], description=row['description'] )
                        saved_items.append(item)
                    except:
                        errors.append(item)
                        print(errors)

                #form = ImportItemsCSVForm()
            return render(request, 'items/import_csv.html', context={'form': form, 'saved_items': saved_items, }, )


class ExportItemsListView(View):
    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="items.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = ['caption', 'image', 'sku', 'price', 'is_active', 'description']
        writer = csv.DictWriter(response, fieldnames=fields_name)
        writer.writeheader()
        for item in Item.objects.iterator():
            writer.writerow(
                {
                    'caption': item.caption,
                    'image': item.image.name if item.image else 'no image',
                    'sku': item.sku,
                    'price': item.price,
                    'is_active': item.is_active,
                    'description': item.description,
                }
            )
        return response
