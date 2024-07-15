from django.db import models
import uuid, os


def contractUpload(instance, filepath):
    ext = os.path.splitext(filepath)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('contracts', filename)

# Create your models here.
class Fabricator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name='Fabricator Name')
    contactPerson = models.CharField(max_length=150, verbose_name='Full Name')
    contactPhone = models.CharField(max_length=13, verbose_name='Contact Number')
    contactCountry = models.CharField(max_length=150, verbose_name='Country')
    contactState = models.CharField(max_length=150, verbose_name='State')
    contactCity = models.CharField(max_length=150, verbose_name='City')
    contract = models.FileField(upload_to=contractUpload, null=True, blank=True, verbose_name='Contract')

    objects = models.Manager()