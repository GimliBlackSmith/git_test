from django.db import models
from django.shortcuts import reverse
import uuid

class Network(models.Model):
    id = models.AutoField(primary_key=True)
    network_address = models.CharField(max_length=20, db_index = True, unique = True)
    uuid = models.UUIDField(default=uuid.uuid4, db_index = True, editable=False)
    
    def get_absolute_url(self):
        return reverse("(delete_network_path)",\
            kwargs={"network_address": self.network_address})
    
    
    def __str__(self):
        return '{}'.format(self.network_address)


class DedicatedAddreses(models.Model):
    id = models.AutoField(primary_key=True)
    network_address = models.CharField(max_length=20, db_index = True)
    dedicated_address = models.CharField(max_length=20, db_index = True, unique = True)
    dedicated_uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index = True)
    avaible = models.CharField(max_length=5, default= "YES")
    address_date = models.DateTimeField(auto_now_add=True)
    #DateField.auto_now - Автоматически устанавливать текущую дату каждый раз, когда объект сохраняется.
    
    def __str__(self):
        return '{}'.format(self.dedicated_address)
    
    
    
    #python manage.py makemigrations
    #python manage.py migrate
