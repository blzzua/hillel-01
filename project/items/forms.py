from django import forms

from items.models import Item


# class ItemsForm(forms.Form):
#     caption = forms.CharField()
#     description = forms.CharField()
#     sku = forms.CharField()
#     price = forms.DecimalField()
#     #image = forms.ImageField()
#
#     def save(self):
#         pass

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('caption', 'description', 'sku', 'price')
