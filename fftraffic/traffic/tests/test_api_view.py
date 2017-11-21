import json

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

client = Client()


class UpdateViewTest(TestCase):
    def setUp(self):
        self.first_update = {
            "scanner": "vultr1",
            "room": "PS",
            "tables": [
                {
                    "name": "Aenna",
                    "player_count": 7,
                    "average_pot": 25.0,
                    "players_per_flop": 13,
                    "hands_per_hour": 221,
                    "unique_player_count": 4,
                    "entry_count": 7,
                    "players": [
                        {
                            "name": "albert1804",
                            "country": "RU",
                            "entries": 1
                        },
                        {
                            "name": "AMMADNAV",
                            "country": "BE",
                            "entries": 4
                        },
                        {
                            "name": "Beebu",
                            "country": "DE",
                            "entries": 1
                        },
                        {
                            "name": "Birdman8883",
                            "country": "GB",
                            "entries": 1
                        },
                    ],
                },
                {
                    "name": "Arp",
                    "player_count": 0,
                    "average_pot": 0,
                    "players_per_flop": 0,
                    "hands_per_hour": 0,
                    "unique_player_count": 0,
                    "entry_count": 0,
                    "players": []
                },
                {
                    "name": "Baade",
                    "player_count": 9,
                    "average_pot": 6.0,
                    "players_per_flop": 17,
                    "hands_per_hour": 238,
                    "unique_player_count": 7,
                    "entry_count": 9,
                    "players": [
                        {
                            "name": "$teve45",
                            "country": "DE",
                            "entries": 1
                        },
                        {
                            "name": "42naGrig",
                            "country": "RU",
                            "entries": 1
                        },
                        {
                            "name": "77kol0bok77",
                            "country": "RU",
                            "entries": 2
                        },
                        {
                            "name": "aaasss422",
                            "country": "DE",
                            "entries": 1
                        },
                        {
                            "name": "aachief775",
                            "country": "AM",
                            "entries": 1
                        },
                        {
                            "name": "agent00723",
                            "country": "RU",
                            "entries": 1
                        },
                        {
                            "name": "Ahimas_VeIde",
                            "country": "UA",
                            "entries": 2
                        },
                    ],
                },

            ],
        }

    def _test_first_update(self):
        response = client.put(reverse('traffic:update_scans'),
                              data=json.dumps(self.first_update),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
