from django.contrib import admin
from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):  
    list_display = ("name",  "price", "opentime","closetime", "latitude","longitude","description",
                    "street_address","city","state","postal_code","country")


admin.site.register(Restaurant, RestaurantAdmin)

