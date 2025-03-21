from django import forms
from django.core.exceptions import ValidationError
from .models import Restaurant
from geopy.geocoders import Nominatim

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'cuisine_type', 
            'phone', 'email', 'website',
            'price_range','average_rating', 'opentime', 'closetime',
            'delivery_available', 'takeout_available',
            'latitude', 'longitude', 'street_address', 'city', 
            'state', 'postal_code', 'country',
        ]
        # Exclude auto-generated fields and fields that should be managed by admin
        exclude = ['id', 'created_at', 'updated_at', 'approved', 'submitted_by']

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        address_fields = [
            cleaned_data.get("street_address"),
            cleaned_data.get("city"),
            cleaned_data.get("state"),
            cleaned_data.get("postal_code"),
            cleaned_data.get("country"),
        ]
        address_provided = any(address_fields)

        if not ((latitude and longitude) or address_provided):
            raise ValidationError("You must provide either coordinates or an address.")

        # If only an address is provided, try to geocode it
        if address_provided and not (latitude and longitude):
            geolocator = Nominatim(user_agent="restaurant_locator")
            address = ", ".join(filter(None, address_fields))
            location = geolocator.geocode(address)

            if location:
                cleaned_data["latitude"] = location.latitude
                cleaned_data["longitude"] = location.longitude
            else:
                raise ValidationError("Could not determine coordinates from address. Please check the address.")

        return cleaned_data
