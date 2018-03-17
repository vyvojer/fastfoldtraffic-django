from datetime import timedelta

from django.utils import timezone
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
        self.scan_0 = Scan.objects.create(scanner=self.scanner, end_datetime=timezone.now())
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


class TableViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.albania = Country.objects.create(iso='AL', name='Albania')
        cls.nigeria = Country.objects.create(iso='NI', name='Nigeria')
        cls.pushkin = Player.objects.create(name='pushkin', country=cls.nigeria, room='PS')
        cls.obama = Player.objects.create(name='obama', country=cls.nigeria, room='PS')
        cls.lenin = Player.objects.create(name='lenin', country=cls.albania, room='PS')
        cls.jackson = Player.objects.create(name='jackson', country=cls.nigeria, room='PS')
        cls.grinder = Player.objects.create(name='grinder', country=cls.nigeria, room='PS')
        cls.gotha = Table.objects.create(room='PS', name='Gotha', game='PLO', limit=100, max_players=6)
        cls.diotima = Table.objects.create(room='PS', name='Diotima', game='PLO', limit=200, max_players=6)
        cls.scanner = Scanner.objects.create(name='Scanner1')
        now = timezone.now()
        cls.now = now
        cls.one_hour_before = now - timedelta(hours=1)
        cls.two_hours_before = now - timedelta(hours=2)
        cls.three_hours_before = now - timedelta(hours=3)
        cls.two_days_before = now - timedelta(days=2)
        cls.three_days_before = now - timedelta(days=3)

    def scan_tree_days_before(self):
        scan = Scan.objects.create(scanner=self.scanner, room='PS')
        table_scan = TableScan.objects.create(scan=scan,
                                 table=self.gotha,
                                 datetime=self.three_days_before,
                                 player_count=6,
                                 average_pot=25,
                                 players_per_flop=30,
                                 unique_player_count=3,
                                 entry_count=6)
        PlayerScan.objects.create(table_scan=table_scan, player=self.pushkin)
        PlayerScan.objects.create(table_scan=table_scan, player=self.jackson)
        PlayerScan.objects.create(table_scan=table_scan, player=self.grinder, entries=4)
        table_scan.save()

    def scan_two_days_before(self):
        scan = Scan.objects.create(scanner=self.scanner, room='PS')
        table_scan = TableScan.objects.create(scan=scan,
                                 table=self.gotha,
                                 datetime=self.two_days_before,
                                 player_count=4,
                                 average_pot=20,
                                 players_per_flop=20,
                                 unique_player_count=2,
                                 entry_count=4)
        PlayerScan.objects.create(table_scan=table_scan, player=self.pushkin)
        PlayerScan.objects.create(table_scan=table_scan, player=self.grinder, entries=3)
        table_scan.save()

    def scan_three_hours_before(self):
        scan = Scan.objects.create(scanner=self.scanner, room='PS')
        table_scan = TableScan.objects.create(scan=scan,
                                 table=self.gotha,
                                 datetime=self.three_hours_before,
                                 player_count=12,
                                 average_pot=30,
                                 players_per_flop=25,
                                 unique_player_count=4,
                                 entry_count=12)
        PlayerScan.objects.create(table_scan=table_scan, player=self.lenin, entries=1)
        PlayerScan.objects.create(table_scan=table_scan, player=self.pushkin, entries=4)
        PlayerScan.objects.create(table_scan=table_scan, player=self.jackson, entries=3)
        PlayerScan.objects.create(table_scan=table_scan, player=self.grinder, entries=4)
        table_scan.save()

    def scan_two_hours_before(self):
        scan = Scan.objects.create(scanner=self.scanner, room='PS')
        table_scan = TableScan.objects.create(scan=scan,
                                 table=self.gotha,
                                 datetime=self.two_hours_before,
                                 player_count=11,
                                 average_pot=35,
                                 players_per_flop=28,
                                 unique_player_count=4,
                                 entry_count=11)
        PlayerScan.objects.create(table_scan=table_scan, player=self.lenin, entries=1)
        PlayerScan.objects.create(table_scan=table_scan, player=self.pushkin, entries=4)
        PlayerScan.objects.create(table_scan=table_scan, player=self.jackson, entries=2)
        PlayerScan.objects.create(table_scan=table_scan, player=self.grinder, entries=4)
        table_scan.save()

    def scan_one_hour_before(self):
        scan = Scan.objects.create(scanner=self.scanner, room='PS')
        table_scan = TableScan.objects.create(scan=scan,
                                 table=self.gotha,
                                 datetime=self.one_hour_before,
                                 player_count=10,
                                 average_pot=26,
                                 players_per_flop=24,
                                 unique_player_count=3,
                                 entry_count=10)
        PlayerScan.objects.create(table_scan=table_scan, player=self.pushkin, entries=4)
        PlayerScan.objects.create(table_scan=table_scan, player=self.jackson, entries=2)
        PlayerScan.objects.create(table_scan=table_scan, player=self.grinder, entries=4)
        table_scan.save()

    def scan_now(self):
        scan = Scan.objects.create(scanner=self.scanner, room='PS')
        table_scan = TableScan.objects.create(scan=scan,
                                 table=self.gotha,
                                 datetime=self.now,
                                 player_count=13,
                                 average_pot=29,
                                 players_per_flop=26,
                                 unique_player_count=5,
                                 entry_count=13)
        PlayerScan.objects.create(table_scan=table_scan, player=self.lenin, entries=1)
        PlayerScan.objects.create(table_scan=table_scan, player=self.obama, entries=1)
        PlayerScan.objects.create(table_scan=table_scan, player=self.pushkin, entries=4)
        PlayerScan.objects.create(table_scan=table_scan, player=self.jackson, entries=3)
        PlayerScan.objects.create(table_scan=table_scan, player=self.grinder, entries=4)
        table_scan.save()

    def test_view(self):
        self.scan_tree_days_before()
        response = client.get(reverse('traffic:table_current', args=['gotha',]))
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['table'].name, 'Gotha')





