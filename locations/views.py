from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

from .models import Location

def get_location(request):
    city = request.POST.get('city', None)
    state = request.POST.get('state', None)
    country = request.POST.get('country', None)
    lng = request.POST.get('longitude', None)
    lat = request.POST.get('latitude', None)

    location, created = Location.objects.get_or_create(city=city, state=state, country=country)
    success = 'Location found'
    
    if created:
        location.latitude = lat
        location.longitude = lng
        location.save()
        success = 'Location added.'

    data = {
        'success': success
    }

    return JsonResponse(data)

class Example(TemplateView):
    template_name="locations/local.html"

    def GET(self, request):
        return render(request, self.template_name)
