from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="res.home"),#redirect to home
    path('about/',views.about,name="res.about"),   #redirect to about page
    path('search/',views.search,name="res.search"),  #redirect to search page
    path('contact/',views.contact,name="res.contact"), #redirect to contact page
    path('signup',views.signup,name="signup"),#redirect to signup page
    path('signin',views.signin,name="signin"),#redirect home after signin or signup
    path('signout',views.signout,name="signout"),#redirect home after signout
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'), #redirect to home after verification

    path('form',views.location_view,name="res.form"), #redirect to form


    path('restaurant/',views.get_res_list,name="res.res"), #for the restaurant list
    path('restaurant/<int:id>/', views.get_res_detail, name='restaurant_detail'), #for the restaurant detail id
    path('map/',views.get_res_map,name="res.map"),   #for the whole map view of the restaurant
]
