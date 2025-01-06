from django.db import models

# Create your models here.
    
class Restaurant(models.Model):
    name = models.CharField("Restaurant Name", max_length=200)
    description = models.TextField(null=False,blank=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    opentime = models.TimeField("Opening Hour")
    closetime = models.TimeField("Closing Hour")
    latitude = models.FloatField(null=False, blank=True)
    longitude = models.FloatField(null=False, blank=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name