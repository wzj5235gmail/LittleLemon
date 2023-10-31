from django.test import TestCase
from .models import Menu
from .serializers import MenuSerializer
from rest_framework import status
from .models import Menu
from .serializers import MenuSerializer
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient



class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")


class MenuViewTest(TestCase):
    def setUp(self):
        Menu.objects.create(title="Item 1", price=10.0, inventory=1)
        Menu.objects.create(title="Item 2", price=15.0, inventory=2)
        user = User.objects.create(username="guest", password='guest@ll.com')
        Token.objects.create(key='d7b02f21a85740dfc51c2a85891ac1cb931c5d04', user=user)

    def test_getall(self):
        url = reverse("menu")
        client = APIClient()
        token = Token.objects.get(user__username='guest')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url)
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
