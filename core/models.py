import uuid
from django.db import models
from django.contrib.auth.models import User

class Fleet(models.Model):
    name = models.CharField(max_length=100) 
    # one fleet belongs to one user
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fleets')

    class Meta:
        # contraint to ensure unique fleet names per user
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_fleet_per_user')
        ]

    def __str__(self):
        return f"{self.name} (Propriétaire: {self.owner.username})"

class Device(models.Model):
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, related_name='devices')
    # ex os version
    os_version = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Device {self.serial_number}"