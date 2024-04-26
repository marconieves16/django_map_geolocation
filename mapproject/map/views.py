from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Search
from .forms import SearchForm
import folium
import geocoder


# Create your views here.
@login_required
def map_view(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None:
        address.delete()
    # Create Map Object
    m = folium.Map(location=[38, 10], zoom_start=2.4)
    folium.Marker([lat, lng], tooltip="Location", popup=country).add_to(m)
    # Get HTML Presentation
    m = m._repr_html_()
    context = {
        "m": m,
        "form": form,
    }
    return render(request, "map.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("")
