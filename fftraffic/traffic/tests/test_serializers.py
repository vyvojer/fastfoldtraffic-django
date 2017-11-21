import json

from django.test import TestCase

from traffic.serializers import ScanSerializer
from traffic.models import Player, Country, Table, Scan, PlayerScan, TableScan


class ScanSerializerTest(TestCase):
    def setUp(self):
        self.first_update = {
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


    def test_first_update(self):
        scan_serialier = ScanSerializer(data=self.first_update)
        if scan_serialier.is_valid():
            scan_serialier.create(scan_serialier.validated_data)
        scans = Scan.objects.all()
        self.assertEqual(len(scans), 1)
