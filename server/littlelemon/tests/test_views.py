from django.test import TestCase
from restaurant import models, views, serializers
class MenuViewTest(TestCase):

    def setup(self):
        item = models.Menu.objects.create(title='IceCream', price=80, inventory=100)
        self.item_serializer = serializers.MenuSerializer(data=item)
        self.assertEqual(self.item_serializer.data, {'title':'IceCream',
                                                'price':80,
                                                'inventory':100})