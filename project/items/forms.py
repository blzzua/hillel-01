from django import forms
from items.models import Item


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'categories']

    image = forms.ImageField(required=False)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be positive")
        if price > 1000_000:
            raise forms.ValidationError("Price is too expensive")
