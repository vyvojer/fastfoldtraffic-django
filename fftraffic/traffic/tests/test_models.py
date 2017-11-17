from django.test import TestCase
from traffic.models import Country, Player

# Create your tests here.


class PlayerTest(TestCase):

    def test_create(self):
        albania = Country.objects.create(name='Albania')
        putin = Player(room='PS', name='putin', country=albania)
        putin.save()
        player = Player.objects.get(name='putin')
        self.assertEqual(player.name, 'putin')
        self.assertEqual(player.room, 'PS')
        self.assertEqual(player.country.name, 'Albania')
