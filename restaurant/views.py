import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404 , render
from django.contrib.auth.models import User
from base import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from .models import Restaurant
from .forms import RestaurantForm
from geopy.geocoders import Nominatim


# Create your views here.


def home(request):  # home view point
    context = {"title": "Home"}
    return render(
        request,
        "homepage/content/home.html",
        context,
    )


def signup(request):  # signup view
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(
            username=username
        ).exists():  # look for existance username
            messages.error(
                request, "Username already exists! Please try another username."
            )
            return redirect("signup")

        if User.objects.filter(email=email).exists():  # look for existance email
            messages.error(request, "Email already registered!")
            return redirect("signup")

        if len(username) > 15:  # username cannot more than 15 char
            messages.error(request, "Username must be under 15 characters.")
            return redirect("signup")

        if pass1 != pass2:  # look pass1 and pass2 match
            messages.error(request, "Passwords did not match.")
            return redirect("signup")

        if not username.isalnum():  # see username is alphanumeric
            messages.error(request, "Username must be alphanumeric!")
            return redirect("signup")

        # Create user, if all meet requirement
        myuser = User.objects.create_user(
            username=username, email=email, password=pass1
        )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()  # save to database

        # send a message to home page after signup and require user to do confirmation
        messages.success(
            request,
            "Your account has been successfully created. We have sent you a confirmation email; please confirm it to activate your account.",
            "if you did not see the confirmation link, please check your junk folder.",
        )

        # Send confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email @ Foodpicker - Login"
        message2 = render_to_string(
            "verification/email_confirmation.html",
            {
                "name": myuser.username,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                "token": generate_token().make_token(myuser),
            },
        )

        # Rename the EmailMessage variable to avoid confusion
        confirmation_email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        confirmation_email.fail_silently = True
        confirmation_email.send()

        return redirect("signin")

    context = {"title": "Sign Up"}
    return render(request, "homepage/accounts/signup.html", context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect(
                "res.home"
            )  # or any other page to redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("signup")  # or to your login page with an error message
    else:
        return redirect("res.home")  # redirect to home if method is not POST


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully! ")
    return redirect("res.home")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token().check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "You have successfully comfirmed your account")
        return redirect("signin")
    else:
        return render(request, "verification\activation_failed.html")


def get_res_list(
    request,
):  # used to show the restaurnt id or sort out the restaurant using id's
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "title": "Restaurant",
    }
    return render(request, "homepage/content/res.html", context)


def get_res_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    return render(
        request, "homepage/content/restaurant_detail.html", {"restaurant": restaurant}
    )


def get_res_map(request):
    # Get all restaurants from the database
    restaurants = Restaurant.objects.all()

    # Convert restaurant queryset to a JSON-friendly format
    restaurants_json = json.dumps(
        [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "opentime": r.opentime.strftime("%H:%M:%S"),
                "closetime": r.closetime.strftime("%H:%M:%S"),
            }
            for r in restaurants
        ]
    )

    return render(
        request, "homepage/content/map.html", {"restaurants_json": restaurants_json}
    )


def geocode_address(address):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    # Fallback to a default location if geocoding fails
    return 0.0, 0.0  # Default coordinates (e.g., somewhere in the middle of the map)



def location_view(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            # Get the full address from the form
            address = f"{form.cleaned_data['street_address']}, {form.cleaned_data['city']}, {form.cleaned_data['state']}, {form.cleaned_data['country']}"

            # Geocode the address to get latitude and longitude
            latitude, longitude = geocode_address(address)

            if latitude and longitude:
                # If geocoding is successful, assign the coordinates to the form instance
                restaurant = form.save(commit=False)
                restaurant.latitude = latitude
                restaurant.longitude = longitude
                restaurant.save()

                # Render a success page
                return render(
                    request,
                    "homepage/content/form_success.html",
                    {"message": "Restaurant added successfully!"},
                )

            else:
                # If geocoding failed, render an error message
                return render(
                    request,
                    "homepage/content/form_success.html",
                    {
                        "message": "Address could not be geocoded. Please check the address."
                    },
                )

    else:
        form = RestaurantForm()

    return render(request, "homepage/content/form.html", {"form": form})


def contact(request):
    context = {"title": "Contact"}
    return render(request, "homepage/content/contact.html", context)


def about(request):
    context = {"title": "About"}
    return render(request, "homepage/content/about.html", context)


def search(request):
    context = {"title": "Search"}
    return render(request, "homepage/content/search.html", context)
