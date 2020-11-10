from tinymce import HTMLField
from django.db import models
from django.urls import  reverse


# Create your models here.
class Service(models.Model):
    service_title = models.CharField(max_length=250)
    service_overview = models.TextField(max_length=300)
    content = HTMLField()

    def __str__(self):
        return self.service_title

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={
            'id': self.id
        })

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Event(models.Model):
    image = models.ImageField()
    event_title = models.CharField(max_length=400)
    event_overview = models.TextField()
    event_link = models.CharField(max_length=500)


    def __str__(self):
        return self.event_title