from django.db import models

# Create your models here.
class Slider(models.Model):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slider_img')