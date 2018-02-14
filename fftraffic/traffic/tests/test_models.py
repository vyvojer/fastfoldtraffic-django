from django.test import TestCase
from traffic.models import Country, Player, Table, Scanner, Scan, TableScan, PlayerScan

# Create your tests here.


class PlayerTest(TestCase):

    def test_create(self):
        albania = Country.objects.create(iso='AL', name='Albania')
        putin = Player(room='PS', name='putin', country=albania)
        putin.save()
        player = Player.objects.get(name='putin')
        self.assertEqual(player.name, 'putin')
        self.assertEqual(player.room, 'PS')
        self.assertEqual(player.country.name, 'Albania')


class ScanTest(TestCase):

    def setUp(self):
        self.albania = Country.objects.create(iso='AL', name='Albania')
        self.nigeria = Country.objects.create(iso='NI', name='Nigeria')
        self.pushkin = Player.objects.create(name='pushkin', country=self.nigeria)
        self.obama = Player.objects.create(name='obama', country=self.nigeria, room='PS')
        self.lenin = Player.objects.create(name='lenin', country=self.albania, room='PS')
        self.aquarium = Table.objects.create(name='Aquarium')
        self.kino = Table.objects.create(name='Kino')
        self.scanner = Scanner.objects.create(ip='192.168.0.1', name='main')
        self.scan_0 = Scan.objects.create(scanner=self.scanner)
        self.scan_1 = Scan.objects.create(scanner=self.scanner)
        self.table_scan_0_aquarium = TableScan.objects.create(scan=self.scan_0, table=self.aquarium, player_count=2)
        self.table_scan_0_kino = TableScan.objects.create(scan=self.scan_0, table=self.kino, player_count=2)
        self.table_scan_1_aquarium = TableScan.objects.create(scan=self.scan_1, table=self.aquarium, player_count=3)
        self.table_scan_1_kino = TableScan.objects.create(scan=self.scan_1, table=self.kino, player_count=3)

    def test_scan(self):
        self.assertEqual(self.scanner.scans.all()[0], self.scan_0)
        self.assertEqual(self.scanner.scans.all()[1], self.scan_1)
        self.assertEqual(list(self.aquarium.scans.all()), [self.table_scan_0_aquarium, self.table_scan_1_aquarium])

    def test_table_last_scan(self):
        self.assertEqual(self.aquarium.last_scan, self.table_scan_1_aquarium)
        self.assertEqual(self.kino.last_scan, self.table_scan_1_kino)

