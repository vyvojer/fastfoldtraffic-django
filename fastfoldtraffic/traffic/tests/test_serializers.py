import json

from django.test import TestCase

from traffic.serializers import ScanSerializer
from traffic.models import Player, Country, Table, Scanner, Scan, PlayerScan, TableScan


class ScanSerializerTest(TestCase):
    def setUp(self):
        self.first_update = {
            "scanner_name": "vultr1",
            "room": "PS",
            "datetime": "2017-11-24T01:24:25.843489",
            "tables": [
                {
                    "name": "Aenna",
                    "player_count": 8,
                    "average_pot": 25.0,
                    "players_per_flop": 13,
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
                    "unique_player_count": 0,
                    "entry_count": 0,
                    "players": []
                },
                {
                    "name": "Baade",
                    "player_count": 9,
                    "average_pot": 6.0,
                    "players_per_flop": 17,
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
                            "country": None,
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
        self.second_update = {
            "scanner_name": "vultr1",
            "room": "PS",
            "datetime": "2017-11-24T01:23:25.843489",
            "tables": [
                {
                    "name": "Arp",
                    "player_count": 0,
                    "average_pot": 0,
                    "players_per_flop": 0,
                    "unique_player_count": 0,
                    "entry_count": 0,
                    "players": []
                },
                {
                    "name": "Lupus",
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
                    "unique_player_count": 7,
                    "entry_count": 9,
                    "players": [
                        {
                            "name": "$teve45",
                            "country": "DE",
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
        self.bad_table = {
            "scanner_name": "vultr1",
            "room": "PS",
            "datetime": "2017-11-24T01:23:25.843489",
            "tables": [
                {
                    "name": "Aenna",
                    "player_count": 8,
                    "average_pot": 25.0,
                    "players_per_flop": 13,
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
                    "name": "Pupu",
                    "player_count": 0,
                    "average_pot": 0,
                    "players_per_flop": 0,
                    "unique_player_count": 0,
                    "entry_count": 0,
                    "players": []
                },
            ],
        }

    def test_first_update(self):
        scan_serialier = ScanSerializer(data=self.first_update)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        scanners = Scanner.objects.all()
        self.assertEqual(len(scanners), 1)
        scans = Scan.objects.all()
        self.assertEqual(len(scans), 1)
        self.assertEqual(scans[0].scanner, scanners[0])
        scan = scans[0]
        self.assertEqual(scan.datetime.year, 2017)
        self.assertEqual(scan.datetime.month, 11)
        self.assertEqual(scan.datetime.day, 24)
        tables = Table.objects.all()
        self.assertEqual(len(tables), 3)
        table_scans = TableScan.objects.all()
        self.assertEqual(len(table_scans), 3)
        self.assertEqual(table_scans[0].table.name, 'Aenna')
        self.assertEqual(table_scans[0].entry_count, 7)
        countries = Country.objects.all()
        self.assertEqual(len(countries), 7)
        players = Player.objects.all()
        self.assertEqual(len(players), 11)
        player_scans = Player.objects.all()
        self.assertEqual(len(player_scans), 11)

        aenna = Table.objects.get(name='Aenna')
        self.assertEqual(aenna.last_scan.scan, scans[0])
        self.assertEqual(aenna.last_scan.player_count, 8)
        self.assertEqual(aenna.last_scan.average_pot, 25.0)
        self.assertEqual(aenna.last_scan.players_per_flop, 13)
        self.assertEqual(aenna.last_scan.unique_player_count, 4)
        self.assertEqual(aenna.last_scan.entry_count, 7)

        kolobok = Player.objects.get(name='77kol0bok77')
        self.assertEqual(kolobok.country.iso, 'UC')

    def test_second_update(self):
        scan_serializer = ScanSerializer(data=self.first_update)
        if scan_serializer.is_valid():
            scan_serializer.update(None, scan_serializer.validated_data)
        scan_serializer = ScanSerializer(data=self.second_update)
        if scan_serializer.is_valid():
            scan_serializer.update(None, scan_serializer.validated_data)
        scanners = Scanner.objects.all()
        self.assertEqual(len(scanners), 1)
        scans = Scan.objects.all()
        self.assertEqual(len(scans), 2)

        baade = Table.objects.get(name='Baade')
        self.assertEqual(baade.last_scan.scan, scans[0])  # first update is older than second

        kolobok = Player.objects.get(name='77kol0bok77')
        self.assertEqual(kolobok.country.iso, 'RU')

    def test_bad_table(self):
        scan_serializer = ScanSerializer(data=self.bad_table)
        if scan_serializer.is_valid():
            scan_serializer.update(None, scan_serializer.validated_data)
        tables = Table.objects.all()
        self.assertEqual(len(tables), 1)

