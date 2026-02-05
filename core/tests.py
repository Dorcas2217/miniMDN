import uuid
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Fleet, Device
class FleetAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("user1", password="pass")
        self.user2 = User.objects.create_user("user2", password="pass")

        self.fleet1 = Fleet.objects.create(
            name="Fleet A",
            owner=self.user1
        )
        Fleet.objects.create(
            name="Fleet B",
            owner=self.user2
        )

        token = Token.objects.create(user=self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key
        )

    def test_user_sees_only_own_fleets(self):
        response = self.client.get("/api/fleets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Fleet A")

class DeviceAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("user1", password="pass")
        self.user2 = User.objects.create_user("user2", password="pass")

        self.fleet1 = Fleet.objects.create(
            name="Fleet A",
            owner=self.user1
        )
        self.fleet2 = Fleet.objects.create(
            name="Fleet B",
            owner=self.user2
        )

        self.device = Device.objects.create(
            serial_number=uuid.uuid4(),
            fleet=self.fleet1
        )

        token = Token.objects.create(user=self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key
        )

    def test_user_can_list_own_devices(self):
        response = self.client.get("/api/devices/")
        self.assertEqual(len(response.data), 1)

    def test_cannot_access_other_user_device(self):
        token = Token.objects.create(user=self.user2)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key
        )

        response = self.client.get(f"/api/devices/{self.device.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_create_device_in_other_fleet(self):
        payload = {
            "serial_number": str(uuid.uuid4()),
            "fleet": self.fleet2.id
        }

        response = self.client.post("/api/devices/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


