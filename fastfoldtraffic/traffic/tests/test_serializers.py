import json

from django.test import TestCase

from traffic.serializers import ScanSerializer
from traffic.models import Player, Country, Table, Scanner, Scan, PlayerScan, TableScan

SCANNER_1_SCAN_1_1 = {
    "scanner_name": "vultr1",
    "full": True,
    "room": "PS",
    "start_datetime": "2017-11-24T01:04:25.843489",
    "end_datetime": "2017-11-24T01:14:25.843489",
    "tables": [
        {
            "name": "Aenna",
            "player_count": 8,
            "average_pot": 25.0,
            "players_per_flop": 13,
            "unique_player_count": 4,
            "entry_count": 7,
            "datetime": "2017-11-24T01:04:35.843489",
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
            "datetime": "2017-11-24T01:08:35.843489",
            "players": []
        },
        {
            "name": "Baade",
            "player_count": 9,
            "average_pot": 6.0,
            "players_per_flop": 17,
            "unique_player_count": 7,
            "entry_count": 9,
            "datetime": "2017-11-24T01:12:35.843489",
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

SCANNER_1_SCAN_1_2 = {
    "scanner_name": "vultr1",
    "full": True,
    "room": "PS",
    "start_datetime": "2017-11-24T01:04:25.843489",
    "end_datetime": "2017-11-24T01:34:25.843489",
    "tables": [
        {
            "name": "Diotima",
            "player_count": 3,
            "average_pot": 60.0,
            "players_per_flop": 28,
            "unique_player_count": 3,
            "entry_count": 4,
            "datetime": "2017-11-24T01:31:25.843489",
            "players": [
                {
                    "name": "19teddyboy89",
                    "country": "GB",
                    "entries": 1
                },
                {
                    "name": "3s4o5r",
                    "country": "CA",
                    "entries": 2
                },
                {
                    "name": "ASLAN_LEV07",
                    "country": "RU",
                    "entries": 1
                },

            ],
        },
    ],
}

SCANNER_2_SCAN_1_1 = {
    "scanner_name": "vultr2",
    "full": False,
    "room": "PS",
    "start_datetime": "2017-11-24T01:04:25.843489",
    "end_datetime": "2017-11-24T01:25:25.843489",
    "tables": [
        {
            "name": "Aenna",
            "player_count": 2,
            "average_pot": 40.0,
            "players_per_flop": 10,
            "unique_player_count": 2,
            "entry_count": 3,
            "datetime": "2017-11-24T01:05:35.843489",
            "players": [
                {
                    "name": "albert1804",
                    "country": "RU",
                    "entries": 1
                },
                {
                    "name": "AMMADNAV",
                    "country": "BE",
                    "entries": 2
                },
            ],
        },

        {
            "name": "Baade",
            "player_count": 9,
            "average_pot": 6.0,
            "players_per_flop": 17,
            "unique_player_count": 7,
            "entry_count": 9,
            "datetime": "2017-11-24T01:06:35.843489",
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

SCANNER_1_SCAN_1_3 = {
    "scanner_name": "vultr1",
    "full": True,
    "room": "PS",
    "start_datetime": "2017-11-24T01:04:25.843489",
    "end_datetime": "2017-11-24T01:54:25.843489",
    "tables": [
        {
            "name": "Gotha",
            "player_count": 8,
            "average_pot": 30.0,
            "players_per_flop": 28,
            "unique_player_count": 13,
            "entry_count": 91,
            "datetime": "2017-11-24T01:53:25.843489",
            "players": [
                {
                    "name": "10YURA10",
                    "country": "UA",
                    "entries": 1
                },
                {
                    "name": "Balamars",
                    "country": "BR",
                    "entries": 1
                },
                {
                    "name": "basilis999",
                    "country": "GR",
                    "entries": 1
                },
                {
                    "name": "BrickT63",
                    "country": "GB",
                    "entries": 4
                },
                {
                    "name": "bunnyx3",
                    "country": "GB",
                    "entries": 3
                },
                {
                    "name": "busch_1992",
                    "country": "AT",
                    "entries": 1
                },
                {
                    "name": "cersenin",
                    "country": "RO",
                    "entries": 2
                },

            ],
        },
    ],
}

SCANNER_1_SCAN_2_1 = {
    "scanner_name": "vultr1",
    "full": True,
    "room": "PS",
    "start_datetime": "2017-11-24T02:05:25.843489",
    "end_datetime": "2017-11-24T02:16:25.843489",
    "tables": [
        {
            "name": "Aenna",
            "player_count": 5,
            "average_pot": 20,
            "players_per_flop": 30,
            "unique_player_count": 3,
            "entry_count": 3,
            "datetime": "2017-11-24T02:05:35.843489",
            "players": [
                {
                    "name": "albert1804",
                    "country": "RU",
                    "entries": 1
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
            "datetime": "2017-11-24T02:09:35.843489",
            "players": []
        },
        {
            "name": "Baade",
            "player_count": 9,
            "average_pot": 6.0,
            "players_per_flop": 17,
            "unique_player_count": 7,
            "entry_count": 9,
            "datetime": "2017-11-24T02:13:35.843489",
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

SCANNER_1_SCAN_2_2 = {
    "scanner_name": "vultr1",
    "full": True,
    "room": "PS",
    "start_datetime": "2017-11-24T02:05:25.843489",
    "end_datetime": "2017-11-24T02:35:25.843489",
    "tables": [
        {
            "name": "Diotima",
            "player_count": 7,
            "average_pot": 55.0,
            "players_per_flop": 22,
            "unique_player_count": 6,
            "entry_count": 7,
            "datetime": "2017-11-24T02:32:25.843489",
            "players": [
                {
                    "name": "19teddyboy89",
                    "country": "GB",
                    "entries": 1
                },
                {
                    "name": "3s4o5r",
                    "country": "CA",
                    "entries": 2
                },
                {
                    "name": "ASLAN_LEV07",
                    "country": "RU",
                    "entries": 1
                },
                {
                    "name": "avyaaa",
                    "country": "CH",
                    "entries": 1
                },
                {
                    "name": "bombmingo",
                    "country": "CH",
                    "entries": 1
                },
                {
                    "name": "Camikadzzzze",
                    "country": "RU",
                    "entries": 1
                },

            ],
        },
    ],
}

SCANNER_1_SCAN_2_3 = {
    "scanner_name": "vultr1",
    "full": True,
    "room": "PS",
    "start_datetime": "2017-11-24T02:05:25.843489",
    "end_datetime": "2017-11-24T02:55:25.843489",
    "tables": [
        {
            "name": "Gotha",
            "player_count": 12,
            "average_pot": 22.0,
            "players_per_flop": 23,
            "unique_player_count": 11,
            "entry_count": 23,
            "datetime": "2017-11-24T02:54:25.843489",
            "players": [
                {
                    "name": "10YURA10",
                    "country": "UA",
                    "entries": 1
                },
                {
                    "name": "Balamars",
                    "country": "BR",
                    "entries": 3
                },
                {
                    "name": "basilis999",
                    "country": "GR",
                    "entries": 1
                },
                {
                    "name": "BrickT63",
                    "country": "GB",
                    "entries": 4
                },
                {
                    "name": "bunnyx3",
                    "country": "GB",
                    "entries": 2
                },
                {
                    "name": "busch_1992",
                    "country": "AT",
                    "entries": 1
                },
                {
                    "name": "cersenin",
                    "country": "RO",
                    "entries": 2
                },
                {
                    "name": "crf88",
                    "country": "GR",
                    "entries": 3
                },
                {
                    "name": "danipesis",
                    "country": "GB",
                    "entries": 4
                },
                {
                    "name": "deeflame7",
                    "country": "DE",
                    "entries": 1
                },
                {
                    "name": "doingtherun",
                    "country": "CA",
                    "entries": 1
                },

            ],
        },
    ],
}

BAD_TABLE_UPDATE = {
    "scanner_name": "vultr1",
    "room": "PS",
    "full": True,
    "start_datetime": "2017-11-22T01:23:25.843489",
    "end_datetime": "2017-11-25T01:23:25.843489",
    "tables": [
        {
            "name": "Aenna",
            "player_count": 8,
            "average_pot": 25.0,
            "players_per_flop": 13,
            "unique_player_count": 4,
            "entry_count": 7,
            "datetime": "2017-11-24T01:23:25.843489",
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
            "datetime": "2017-11-24T01:23:25.843489",
            "players": []
        },
    ],
}


class ScanSerializerTest(TestCase):

    def test_scans(self):
        scan_serialier = ScanSerializer(data=SCANNER_1_SCAN_1_1)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        else:
            print(scan_serialier.error_messages)
        self.scanner_1_scan_1_1()

        scan_serialier = ScanSerializer(data=SCANNER_1_SCAN_1_2)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        self.scanner_1_scan_1_2()

        scan_serialier = ScanSerializer(data=SCANNER_2_SCAN_1_1)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        self.scanner_2_scan_1_1()

        scan_serialier = ScanSerializer(data=SCANNER_1_SCAN_1_3)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        self.scanner_1_scan_1_3()

        scan_serialier = ScanSerializer(data=SCANNER_1_SCAN_2_1)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        self.scanner_1_scan_2_1()

        scan_serialier = ScanSerializer(data=SCANNER_1_SCAN_2_2)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        self.scanner_1_scan_2_2()

        scan_serialier = ScanSerializer(data=SCANNER_1_SCAN_2_3)
        if scan_serialier.is_valid():
            scan_serialier.update(None, scan_serialier.validated_data)
        self.scanner_1_scan_2_3()

    def scanner_1_scan_1_1(self):
        #  Test scanners
        scanners = Scanner.objects.all()
        self.assertEqual(len(scanners), 1)

        # Test scans
        scans = Scan.objects.all()
        scan = scans[0]
        self.assertEqual(len(scans), 1)
        self.assertEqual(scan.scanner, scanners[0])
        self.assertEqual(scan.start_datetime.minute, 4)
        self.assertEqual(scan.end_datetime.minute, 14)
        self.assertEqual(scan.full, True)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 3)

        aenna = Table.objects.get(name='Aenna')
        self.assertEqual(aenna.last_scan.scan, scans[0])
        self.assertEqual(aenna.last_scan.player_count, 8)
        self.assertEqual(aenna.last_scan.average_pot, 25.0)
        self.assertEqual(aenna.last_scan.players_per_flop, 13)
        self.assertEqual(aenna.last_scan.unique_player_count, 4)
        self.assertEqual(aenna.last_scan.entry_count, 7)
        self.assertAlmostEqual(aenna.mtr, 1.75, delta=0.01)
        self.assertAlmostEqual(aenna.avg_pot, 25, delta=0.01)
        self.assertAlmostEqual(aenna.avg_unique_player_count, 4, delta=0.01)
        self.assertAlmostEqual(aenna.avg_entry_count, 7, delta=0.01)
        self.assertAlmostEqual(aenna.avg_mtr, 1.75, delta=0.01)

        # Test table_scans
        table_scans = TableScan.objects.all()
        self.assertEqual(len(table_scans), 3)
        self.assertEqual(table_scans[0].table.name, 'Aenna')
        self.assertEqual(table_scans[0].datetime.year, 2017)
        self.assertEqual(table_scans[0].datetime.minute, 4)
        self.assertEqual(table_scans[0].entry_count, 7)
        self.assertEqual(table_scans[2].table.name, 'Baade')
        self.assertEqual(table_scans[2].datetime.minute, 12)

        # Test countries
        countries = Country.objects.all()
        self.assertEqual(len(countries), 7)
        players = Player.objects.all()
        self.assertEqual(len(players), 11)
        player_scans = Player.objects.all()
        self.assertEqual(len(player_scans), 11)

        # Test players
        kolobok = Player.objects.get(name='77kol0bok77')
        self.assertEqual(kolobok.country.iso, 'UC')

    def scanner_1_scan_1_2(self):

        #  Test scanners
        scanners = Scanner.objects.all()
        self.assertEqual(len(scanners), 1)

        # Test scans
        scans = Scan.objects.all().order_by('end_datetime')
        self.assertEqual(len(scans), 1)
        scan = scans[0]
        self.assertEqual(scan.scanner, scanners[0])
        self.assertEqual(scan.start_datetime.minute, 4)
        self.assertEqual(scan.full, True)
        self.assertEqual(scan.end_datetime.minute, 34)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 4)

        table = Table.objects.get(name='Aenna')
        self.assertEqual(table.last_scan.scan, scans[0])
        self.assertEqual(table.last_scan.player_count, 8)
        self.assertEqual(table.last_scan.average_pot, 25.0)
        self.assertEqual(table.last_scan.players_per_flop, 13)
        self.assertEqual(table.last_scan.unique_player_count, 4)
        self.assertEqual(table.last_scan.entry_count, 7)
        self.assertAlmostEqual(table.mtr, 1.75, delta=0.01)
        self.assertAlmostEqual(table.avg_pot, 25, delta=0.01)
        self.assertAlmostEqual(table.avg_unique_player_count, 4, delta=0.01)
        self.assertAlmostEqual(table.avg_entry_count, 7, delta=0.01)
        self.assertAlmostEqual(table.avg_mtr, 1.75, delta=0.01)

        table = Table.objects.get(name='Diotima')
        self.assertEqual(table.last_scan.scan, scans[0])
        self.assertEqual(table.last_scan.player_count, 3)

        # Test table_scans
        table_scans = TableScan.objects.all().order_by('table__name')
        self.assertEqual(len(table_scans), 4)
        self.assertEqual(table_scans[0].table.name, 'Aenna')
        self.assertEqual(table_scans[0].datetime.year, 2017)
        self.assertEqual(table_scans[0].datetime.minute, 4)
        self.assertEqual(table_scans[0].entry_count, 7)
        self.assertEqual(table_scans[2].table.name, 'Baade')
        self.assertEqual(table_scans[2].datetime.minute, 12)
        self.assertEqual(table_scans[3].table.name, 'Diotima')
        self.assertEqual(table_scans[3].datetime.minute, 31)

        # Test countries
        countries = Country.objects.all()
        self.assertEqual(len(countries), 8)

        # Test players
        players = Player.objects.all()
        self.assertEqual(len(players), 14)
        kolobok = Player.objects.get(name='77kol0bok77')
        self.assertEqual(kolobok.country.iso, 'UC')

    def scanner_2_scan_1_1(self):

        #  Test scanners
        scanners = Scanner.objects.all().order_by('name')
        self.assertEqual(len(scanners), 2)

        # Test scans
        scans = Scan.objects.all().order_by('scanner__name', 'end_datetime')
        self.assertEqual(len(scans), 2)
        scan = Scan.objects.get(scanner__name='vultr2')
        self.assertEqual(scan.scanner, scanners[1])
        self.assertEqual(scan.start_datetime.minute, 4)
        self.assertEqual(scan.full, False)
        self.assertEqual(scan.end_datetime.minute, 25)

        self.assertEqual(len(Scan.objects.filter(full=True)), 1)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 4)

        table = Table.objects.get(name='Aenna')
        self.assertEqual(table.last_scan.scan, scans[1])
        self.assertEqual(table.last_scan.player_count, 2)
        self.assertEqual(table.last_scan.average_pot, 40.0)
        self.assertEqual(table.last_scan.players_per_flop, 10)
        self.assertEqual(table.last_scan.unique_player_count, 2)
        self.assertEqual(table.last_scan.entry_count, 3)
        self.assertAlmostEqual(table.mtr, 1.5, delta=0.01)
        self.assertAlmostEqual(table.avg_pot, 32.5, delta=0.01)
        self.assertAlmostEqual(table.avg_unique_player_count, 3, delta=0.01)
        self.assertAlmostEqual(table.avg_entry_count, 5, delta=0.01)
        self.assertAlmostEqual(table.avg_mtr, 1.6667, delta=0.01)

        table = Table.objects.get(name='Diotima')
        self.assertEqual(table.last_scan.scan, scans[0])
        self.assertEqual(table.last_scan.player_count, 3)

        # Test table_scans
        table_scans = TableScan.objects.all().order_by('table__name', 'datetime')
        self.assertEqual(len(table_scans), 6)
        self.assertEqual(table_scans[0].table.name, 'Aenna')
        self.assertEqual(table_scans[0].datetime.year, 2017)
        self.assertEqual(table_scans[0].datetime.minute, 4)
        self.assertEqual(table_scans[1].table.name, 'Aenna')
        self.assertEqual(table_scans[1].datetime.year, 2017)
        self.assertEqual(table_scans[1].datetime.minute, 5)


        # Test countries
        countries = Country.objects.all()
        self.assertEqual(len(countries), 8)

        # Test players
        players = Player.objects.all()
        self.assertEqual(len(players), 14)
        kolobok = Player.objects.get(name='77kol0bok77')
        self.assertEqual(kolobok.country.iso, 'UC')

    def scanner_1_scan_1_3(self):

        #  Test scanners
        scanners = Scanner.objects.all().order_by('name')
        self.assertEqual(len(scanners), 2)

        # Test scans
        scans = Scan.objects.all().order_by('scanner__name', 'end_datetime')
        self.assertEqual(len(scans), 2)
        scan = Scan.objects.get(scanner__name='vultr1')
        self.assertEqual(scan.scanner, scanners[0])
        self.assertEqual(scan.start_datetime.minute, 4)
        self.assertEqual(scan.full, True)
        self.assertEqual(scan.end_datetime.minute, 54)

        self.assertEqual(len(Scan.objects.filter(full=True)), 1)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 5)

        table = Table.objects.get(name='Gotha')
        self.assertEqual(table.last_scan.scan, scans[0])
        self.assertEqual(table.last_scan.player_count, 8)

        # Test table_scans
        table_scans = TableScan.objects.all().order_by('table__name', 'datetime')
        self.assertEqual(len(table_scans), 7)

    def scanner_1_scan_2_1(self):

        #  Test scanners
        scanners = Scanner.objects.all().order_by('name')
        self.assertEqual(len(scanners), 2)

        # Test scans
        scans = Scan.objects.all().order_by('scanner__name', 'end_datetime')
        self.assertEqual(len(scans), 3)
        scan = Scan.objects.filter(scanner__name='vultr1').order_by('end_datetime')[1]
        self.assertEqual(scan.scanner, scanners[0])
        self.assertEqual(scan.start_datetime.minute, 5)
        self.assertEqual(scan.full, True)
        self.assertEqual(scan.end_datetime.minute, 16)

        self.assertEqual(len(Scan.objects.filter(full=True)), 2)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 5)

        table = Table.objects.get(name='Aenna')
        self.assertEqual(table.last_scan.scan, scans[1])
        self.assertEqual(table.last_scan.player_count, 5)
        self.assertEqual(table.last_scan.average_pot, 20.0)
        self.assertEqual(table.last_scan.players_per_flop, 30)
        self.assertEqual(table.last_scan.unique_player_count, 3)
        self.assertEqual(table.last_scan.entry_count, 3)
        self.assertAlmostEqual(table.mtr, 1, delta=0.01)
        self.assertAlmostEqual(table.avg_pot, 28.3333, delta=0.01)
        self.assertAlmostEqual(table.avg_unique_player_count, 3, delta=0.01)
        self.assertAlmostEqual(table.avg_entry_count, 4.33333, delta=0.01)
        self.assertAlmostEqual(table.avg_mtr, 1.4444, delta=0.01)

        table = Table.objects.get(name='Gotha')
        self.assertEqual(table.last_scan.scan, scans[0])
        self.assertEqual(table.last_scan.player_count, 8)

        # Test table_scans
        table_scans = TableScan.objects.all().order_by('table__name', 'datetime')
        self.assertEqual(len(table_scans), 10)

    def scanner_1_scan_2_2(self):

        #  Test scanners
        scanners = Scanner.objects.all().order_by('name')
        self.assertEqual(len(scanners), 2)

        # Test scans
        scans = Scan.objects.all().order_by('scanner__name', 'end_datetime')
        self.assertEqual(len(scans), 3)
        scan = Scan.objects.filter(scanner__name='vultr1').order_by('end_datetime')[1]
        self.assertEqual(scan.scanner, scanners[0])
        self.assertEqual(scan.start_datetime.minute, 5)
        self.assertEqual(scan.full, True)
        self.assertEqual(scan.end_datetime.minute, 35)

        self.assertEqual(len(Scan.objects.filter(full=True)), 2)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 5)

        table = Table.objects.get(name='Gotha')
        self.assertEqual(table.last_scan.scan, scans[0])
        self.assertEqual(table.last_scan.datetime.minute, 53)
        self.assertEqual(table.last_scan.player_count, 8)

        # Test table_scans
        table_scans = TableScan.objects.all().order_by('table__name', 'datetime')
        self.assertEqual(len(table_scans), 11)

    def scanner_1_scan_2_3(self):

        #  Test scanners
        scanners = Scanner.objects.all().order_by('name')
        self.assertEqual(len(scanners), 2)

        # Test scans
        scans = Scan.objects.all().order_by('scanner__name', 'end_datetime')
        self.assertEqual(len(scans), 3)
        scan = Scan.objects.filter(scanner__name='vultr1').order_by('end_datetime')[1]
        self.assertEqual(scan.scanner, scanners[0])
        self.assertEqual(scan.start_datetime.minute, 5)
        self.assertEqual(scan.full, True)
        self.assertEqual(scan.end_datetime.minute, 55)

        self.assertEqual(len(Scan.objects.filter(full=True)), 2)

        # Test tables
        tables = Table.objects.all()
        self.assertEqual(len(tables), 5)

        table = Table.objects.get(name='Gotha')
        self.assertEqual(table.last_scan.scan, scans[1])
        self.assertEqual(table.last_scan.datetime.minute, 54)
        self.assertEqual(table.last_scan.player_count, 12)

        # Test table_scans
        table_scans = TableScan.objects.all().order_by('table__name', 'datetime')
        self.assertEqual(len(table_scans), 12)

    def test_bad_table(self):
        scan_serializer = ScanSerializer(data=BAD_TABLE_UPDATE)
        if scan_serializer.is_valid():
            scan_serializer.update(None, scan_serializer.validated_data)
        tables = Table.objects.all()
        self.assertEqual(len(tables), 1)
