from django import forms
from items.models import Item


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
