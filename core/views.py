from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Fleet, Device
from .serializers import UserSerializer, FleetSerializer, DeviceSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List of users. contains fleets owned by each user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class FleetViewSet(viewsets.ModelViewSet):
    """
    Fleet management. A user can only see their own fleets.
    """
    serializer_class = FleetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Fleet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DeviceViewSet(viewsets.ModelViewSet):
    """
    Device management : Users can only see devices in their own fleets.
    """
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fleet'] #use to filter devices by fleet

    def get_queryset(self):
        # get only devices in fleets owned by the user
        return Device.objects.filter(fleet__owner=self.request.user)

    def perform_create(self, serializer):
        # Ensure the fleet belongs to the user
        fleet = serializer.validated_data['fleet']
        if fleet.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("you cannot add devices to fleets you do not own.")
        serializer.save()
