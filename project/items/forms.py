import csv

from django import forms
from items.models import Item
from django.core.exceptions import ValidationError


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'categories']

    description = forms.CharField(widget=forms.Textarea(attrs={"cols": "10", "rows": "5", 'class': 'form-control display-4'}))
    image = forms.ImageField(required=False)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be positive")
        if price > 1000_000:
            raise forms.ValidationError("Price is too expensive")
        return price





class ImportItemsCSVForm(forms.Form):
    csv_file = forms.FileField()
    ON_DUPLICATE_CHOICES = (
        ('update', 'UPDATE'),
        ('ignore', 'IGNORE'),
        ('abort', 'ABORT'),
    )

    on_duplicate = forms.ChoiceField(choices=ON_DUPLICATE_CHOICES, widget=forms.Select())
    # replace_duplicate = forms.BooleanField(required=False)
    single_transaction = forms.BooleanField(required=False)
    on_duplicate.widget.attrs.update({"title": "Action on duplicate caption"})
    single_transaction.widget.attrs.update({"checked":  True, "title": "rollback on any errors."})

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        csv_file.seek(0)
        dict_reader = csv.DictReader(decoded_file)
        required_fields = ['caption', 'sku', 'price', 'is_active', 'description']
        for field in required_fields:
            if field not in dict_reader.fieldnames:
                raise ValidationError(f'CSV file is missing required field: {field}')

        return csv_file
