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
        fields = ['name', 'description', 'price', 'opentime','closetime', 'latitude', 'longitude','street_address','city','state','postal_code','country']
        labels = {
            "name":"Please enter your restaurant name",
            "description":"Please enter a description",
            "price":"Please enter the price",
            "opentime":"Please enter the opening time",
            "closetime":"Please enter the closing time",
            "latitude":"Please enter the latitude",
            "longitude":"Please enter the longitude",
            "street_address":"Please enter the street address",
            "city":"Please enter the city",
            "state":"Please enter the state",
            "postal_code":"Please enter the postal code",
            "country":"Please enter the country",


        }
        

    
    

        
