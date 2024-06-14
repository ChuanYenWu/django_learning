from django.contrib import admin
from .models import LunchboxModel, BuyingModel
# Register your models here.
#admin.site.register(LunchboxModel)
#admin.site.register(BuyingModel)

@admin.register(LunchboxModel)
class LunchboxAdmin(admin.ModelAdmin):
    list_display = ('lunchbox_name', 'lunchbox_cost')

@admin.register(BuyingModel)
class BuyingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'meat_num', 'vege_num', 'total_cost', 'buytime')