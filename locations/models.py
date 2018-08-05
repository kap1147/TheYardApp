from django.db import models

class LocationManager(models.Manager):

    def create_new(self, data):
        location = self.model()
        if data is not None:
            city = data['city']
            state = data['region']
            if not Location.objects.filter(city=city, state=state).exists():
                location.city = city
                location.state = state
                location.country = data['country_code']
                location.latitude = data['latitude']
                location.longitude = data['longitude']
                location.save()
                return location
            else:
                return Location.objects.get(city=city, state=state)


class Location(models.Model):
    city        = models.CharField(max_length=120, null=True, blank=True)
    state       = models.CharField(max_length=2, null=True, blank=True)
    country     = models.CharField(max_length=20)
    latitude    = models.FloatField(null=True, blank=True)
    longitude   = models.FloatField(null=True, blank=True)

    objects = LocationManager()

    def __str__(self):
        return '{}, {}'.format(self.city, self.state)

