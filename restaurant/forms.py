from django import forms
from django.core.exceptions import ValidationError
from .models import Restaurant

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        required=True,
    )

 
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'price', 'opentime', 'closetime',
            'latitude', 'longitude', 'street_address', 'city', 
            'state', 'postal_code', 'country'
        ]
        labels = {
            "name": "Please enter your restaurant name",
            "description": "Please enter a description",
            "price": "Please enter the price",
            "opentime": "Please enter the opening time",
            "closetime": "Please enter the closing time",
            "latitude": "Please enter the latitude",
            "longitude": "Please enter the longitude",
            "street_address": "Please enter the street address",
            "city": "Please enter the city",
            "state": "Please enter the state",
            "postal_code": "Please enter the postal code",
            "country": "Please enter the country",
        }

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        street_address = cleaned_data.get("street_address")
        city = cleaned_data.get("city")
        state = cleaned_data.get("state")
        postal_code = cleaned_data.get("postal_code")
        country = cleaned_data.get("country")

        # Determine if the address or coordinates were provided
        address_provided = all([street_address, city, state, postal_code, country])
        coordinates_provided = latitude is not None and longitude is not None

        if address_provided and coordinates_provided:
            raise ValidationError("Please provide either an address or coordinates, not both.")
        
        if not address_provided and not coordinates_provided:
            raise ValidationError("Please provide either an address or coordinates.")

        return cleaned_data
        

    
    

        
