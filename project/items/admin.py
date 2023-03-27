from django.contrib import admin

# Register your models here.
from .models import Item, Category, Discount
# admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Discount)


class SomeInLine(admin.StackedInline):
    model = Item.cats.through
    extra = 1


@admin.register(Item)
class AdminItem(admin.ModelAdmin):
    inlines = [SomeInLine]

    @admin.display(description='cats')
    def list_of_categories(self, cat):
        #  return self.caption
        return cat.get_categories_names()

    list_display = ('id', 'sku', 'caption', 'is_active')
    list_editable = ('caption', 'is_active')
