from django.db import models
import uuid, os

def contractUpload(instance, filepath):
    ext = os.path.splitext(filepath)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('designStandard', filename)

class ContactPerson(models.Model):
    fabricator = models.ForeignKey('Fabricator', on_delete=models.CASCADE, verbose_name='Fabricator')
    name = models.CharField(max_length=150, verbose_name='Full Name', null=True, blank=True)
    designation = models.CharField(max_length=150, verbose_name='Designation', null=True, blank=True)
    phone = models.CharField(max_length=13, verbose_name='Phone Number', null=True, blank=True)
    email = models.EmailField(max_length=150, verbose_name='Email Address', null=True, blank=True)
    objects = models.Manager()


# Create your models here.
class Fabricator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name='Fabricator Name')
    country = models.CharField(max_length=150, verbose_name='Country')
    state = models.CharField(max_length=150, verbose_name='State')
    city = models.CharField(max_length=150, verbose_name='City')
    zipCode = models.CharField(max_length=6, verbose_name='Zip Code')
    design = models.FileField(upload_to=contractUpload, null=True, blank=True)
    objects = models.Manager()


    def get_contact_person(self):
        return ContactPerson.objects.filter(fabricator=self)
    
    def add_contact_person(self, name, designation, phone, email):
        return ContactPerson.objects.create(fabricator=self, name=name, designation=designation, phone=phone, email=email)
    
    def remove_contact_person(self, id):
        return ContactPerson.objects.get(pk=id).delete()
    
    def update_contact_person(self, id, name=None, designation=None, phone=None, email=None):
        contact_person = ContactPerson.objects.get(pk=id)
        if name:
            contact_person.name = name
        if designation:
            contact_person.designation = designation
        if phone:
            contact_person.phone = phone
        if email:
            contact_person.email = email
        contact_person.save()
        return contact_person