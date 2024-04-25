from django.shortcuts import render, redirect
from .models import Search
from .forms import SearchForm
import folium
import geocoder


# Create your views here.
def index(request):
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
    if lat == None or lng == None:
        address.delete()
    else:
        country = location.country
        city = location.city
        print(location.country, location.city)
    # Create Map Object
    m = folium.Map(location=[19, -12], zoom_start=2)
    folium.Marker([lat, lng], tooltip="Location", popup=country).add_to(m)
    # Get HTML Presentation
    m = m._repr_html_()
    context = {
        "m": m,
        "form": form,
    }
    return render(request, "index.html", context)
