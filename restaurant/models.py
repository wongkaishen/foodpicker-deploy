from django.db import models
from geopy.distance import geodesic
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(_("Read"), default=False)
    
    class Meta:
        ordering = ['-created_at'] 
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
    
    def __str__(self):
        return f"{self.subject} - {self.name}"

class Restaurant(models.Model):
    PRICE_CHOICES = [
        ('$', 'Budget'),
        ('$$', 'Moderate'),
        ('$$$', 'Expensive'),
        ('$$$$', 'Fine Dining'),
    ]

    CUISINE_CHOICES = [
        ('ASIAN', 'Asian'),
        ('ITALIAN', 'Italian'),
        ('MEXICAN', 'Mexican'),
        ('AMERICAN', 'American'),
        ('INDIAN', 'Indian'),
        ('MEDITERRANEAN', 'Mediterranean'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(_("Restaurant Name"), max_length=200)
    description = models.TextField(_("Description"))
    cuisine_type = models.CharField(_("Cuisine Type"), max_length=50, choices=CUISINE_CHOICES, default='OTHER')
    
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Website"), blank=True)

    price_range = models.CharField(_("Price Range"), max_length=4, choices=PRICE_CHOICES, default='$$')
    average_rating = models.FloatField(_("Average Rating"), default=0,)

    opentime = models.TimeField(_("Opening Hour"))
    closetime = models.TimeField(_("Closing Hour"))
    delivery_available = models.BooleanField(_("Delivery Available"), default=False)
    takeout_available = models.BooleanField(_("Takeout Available"), default=False)

    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State/Province"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(_("Approved"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        

    def __str__(self):
        return f"{self.name} ({self.city})"

    def approve(self):
        """Mark the restaurant as approved and transfer to ApprovedRestaurant."""
        ApprovedRestaurant.objects.create(
            name=self.name,
            description=self.description,
            cuisine_type=self.cuisine_type,
            phone=self.phone,
            email=self.email,
            website=self.website,
            price_range=self.price_range,
            average_rating=self.average_rating,
            opentime=self.opentime,
            closetime=self.closetime,
            delivery_available=self.delivery_available,
            takeout_available=self.takeout_available,
            latitude=self.latitude,
            longitude=self.longitude,
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country,
            submitted_by=self.submitted_by,
        )
        self.delete()
class ApprovedRestaurant(models.Model):
    name = models.CharField(_("Restaurant Name"), max_length=200, db_index=True)
    description = models.TextField(_("Description"))
    cuisine_type = models.CharField(_("Cuisine Type"), max_length=50, choices=Restaurant.CUISINE_CHOICES, default='OTHER', db_index=True)
    
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Website"), blank=True)

    price_range = models.CharField(_("Price Range"), max_length=4, choices=Restaurant.PRICE_CHOICES, default='$$', db_index=True)
    average_rating = models.FloatField(_("Average Rating"), default=0, db_index=True)

    opentime = models.TimeField(_("Opening Hour"))
    closetime = models.TimeField(_("Closing Hour"))
    delivery_available = models.BooleanField(_("Delivery Available"), default=False, db_index=True)
    takeout_available = models.BooleanField(_("Takeout Available"), default=False, db_index=True)

    latitude = models.FloatField(_("Latitude"), null=True, blank=True, db_index=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True, db_index=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State/Province"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)

    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Approved Restaurant")
        verbose_name_plural = _("Approved Restaurants")

    def __str__(self):
        return f"{self.name} ({self.city})"

