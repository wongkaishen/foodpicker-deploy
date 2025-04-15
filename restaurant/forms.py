from django import forms
from django.core.exceptions import ValidationError
from .models import Restaurant
from geopy.geocoders import Nominatim
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class RestaurantForm(forms.ModelForm):
    opentime = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control flatpickr-time',
                'placeholder': 'Select opening time (24h)',
                'type': 'time',
                'data-input': '',
                'data-enable-time': 'true',
                'data-no-calendar': 'true',
                'data-date-format': "H:i",
                'data-time_24hr': 'true'
            }
        ),
        required=False,
        input_formats=['%H:%M']
    )
    closetime = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control flatpickr-time',
                'placeholder': 'Select closing time (24h)',
                'type': 'time',
                'data-input': '',
                'data-enable-time': 'true',
                'data-no-calendar': 'true',
                'data-date-format': "H:i",
                'data-time_24hr': 'true'
            }
        ),
        required=False,
        input_formats=['%H:%M']
    )

    class Meta:
        model = Restaurant
        fields = [
            'name', 'cuisine_type', 'description',
            'phone', 'email', 'website',
            'price_range', 'average_rating',
            'opentime', 'closetime',
            'delivery_available', 'takeout_available',
            'street_address', 'city', 'state', 'postal_code', 'country',
            'latitude', 'longitude', 'image',  # Added image field
        ]
        exclude = ['id', 'created_at', 'updated_at', 'approved', 'submitted_by']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter restaurant name',
                    'autocomplete': 'off'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe your restaurant...',
                    'rows': 4,
                    'style': 'resize: vertical; min-height: 120px;'
                }
            ),
            'cuisine_type': forms.Select(
                attrs={
                    'class': 'form-control custom-select',
                    'placeholder': 'Select cuisine type'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+60 12-345-6789',
                    'pattern': '[\+]?[0-9\s\-]+',
                    'title': 'Enter a valid phone number'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'restaurant@example.com',
                    'autocomplete': 'off'
                }
            ),
            'website': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://www.example.com',
                    'autocomplete': 'off'
                }
            ),
            'price_range': forms.Select(
                attrs={
                    'class': 'form-control custom-select',
                    'placeholder': 'Select price range'
                }
            ),
            'average_rating': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '4.5',
                    'min': '0',
                    'max': '5',
                    'step': '0.1',
                    'title': 'Enter a rating between 0 and 5'
                }
            ),
            'delivery_available': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input custom-control-input',
                    'role': 'switch'
                }
            ),
            'takeout_available': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input custom-control-input',
                    'role': 'switch'
                }
            ),
            'street_address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '123 Restaurant Street',
                    'autocomplete': 'off'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'City name',
                    'autocomplete': 'off'
                }
            ),
            'state': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'State name',
                    'autocomplete': 'off'
                }
            ),
            'postal_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '50000',
                    'pattern': '[0-9]+',
                    'title': 'Enter a valid postal code'
                }
            ),
            'country': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Malaysia',
                }
            ),
            'latitude': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '3.1390',
                    'step': 'any',

                }
            ),
            'longitude': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '101.6869',
                    'step': 'any',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('cuisine_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('latitude', css_class='form-group col-md-6 mb-0'),
                Column('longitude', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            'street_address',
            'city',
            'state',
            'postal_code',
            'country',
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

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

    def clean_opentime(self):
        opentime = self.cleaned_data.get('opentime')
        if opentime:
            try:
                # opentime is already a time object when using TimeField
                return opentime
            except ValueError:
                raise forms.ValidationError("Invalid time format. Use 24-hour format (HH:MM)")
        return None

    def clean_closetime(self):
        closetime = self.cleaned_data.get('closetime')
        if closetime:
            try:
                # closetime is already a time object when using TimeField
                return closetime
            except ValueError:
                raise forms.ValidationError("Invalid time format. Use 24-hour format (HH:MM)")
        return None
