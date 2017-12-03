from django.test import TestCase, Client
from django.urls import reverse

from traffic.models import Country, Player, Table, Scanner, Scan, TableScan, PlayerScan

client = Client()


class IndexViewTest(TestCase):
    def setUp(self):
        self.albania = Country.objects.create(iso='AL', name='Albania')
        self.nigeria = Country.objects.create(iso='NI', name='Nigeria')
        self.pushkin = Player.objects.create(name='pushkin', country=self.nigeria)
        self.obama = Player.objects.create(name='obama', country=self.nigeria, room='PS')
        self.lenin = Player.objects.create(name='lenin', country=self.albania, room='PS')
        self.scanner = Scanner.objects.create(ip='192.168.0.1', name='main')

    def create_tables(self):
        self.aquarium = Table.objects.create(name='Aquarium')
        self.kino = Table.objects.create(name='Kino')

    def make_first_scan(self):
        self.scan_0 = Scan.objects.create(scanner=self.scanner)
        self.table_scan_0_aquarium = TableScan.objects.create(scan=self.scan_0, table=self.aquarium, entry_count=2,
                                                              player_count=2)
        self.table_scan_0_kino = TableScan.objects.create(scan=self.scan_0, table=self.kino, entry_count=3,
                                                          player_count=3)

    def test_without_any_table(self):
        response = client.get(reverse('traffic:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No scans yet")

    def test_after_first_scan(self):
        self.create_tables()
        self.make_first_scan()
        response = client.get(reverse('traffic:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No scans yet")
        self.assertContains(response, "Aquarium")
        self.assertContains(response, "Kino")
        self.assertEqual(list(response.context['tables']),
                         [self.aquarium,
                          self.kino])
