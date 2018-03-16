from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from traffic.models import *


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
        now = timezone.now()
        self.scan_0 = Scan.objects.create(scanner=self.scanner, end_datetime=now - timedelta(hours=1))
        self.scan_2 = Scan.objects.create(scanner=self.scanner, end_datetime=now + timedelta(hours=1))
        self.scan_1 = Scan.objects.create(scanner=self.scanner, end_datetime=now)
        self.table_scan_0_aquarium = TableScan.objects.create(scan=self.scan_0, table=self.aquarium, player_count=2)
        self.table_scan_0_kino = TableScan.objects.create(scan=self.scan_0, table=self.kino, player_count=2)
        self.table_scan_1_aquarium = TableScan.objects.create(scan=self.scan_1, table=self.aquarium, player_count=3)
        self.table_scan_1_kino = TableScan.objects.create(scan=self.scan_1, table=self.kino, player_count=3)
        self.table_scan_2_aquarium = TableScan.objects.create(scan=self.scan_2, table=self.aquarium, player_count=3)
        self.table_scan_2_kino = TableScan.objects.create(scan=self.scan_2, table=self.kino, player_count=3)

    def test_scan(self):
        self.assertEqual(self.scanner.scans.all()[0], self.scan_0)
        self.assertEqual(self.scanner.scans.all()[1], self.scan_2)
        self.assertEqual(list(self.aquarium.table_scans.all()), [self.table_scan_0_aquarium,
                                                                 self.table_scan_1_aquarium,
                                                                 self.table_scan_2_aquarium])

    def test_table_last_scan(self):
        self.assertEqual(self.aquarium.last_scan, self.table_scan_2_aquarium)
        self.assertEqual(self.kino.last_scan, self.table_scan_2_kino)


class TableTest(TestCase):

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

    def test_tables(self):
        self.scan_tree_days_before()

        self.assertEqual(self.gotha.last_scan.datetime, self.three_days_before)
        self.assertEqual(self.gotha.last_scan.player_count, 6)
        self.assertEqual(self.gotha.last_scan.average_pot, 25)
        self.assertEqual(self.gotha.last_scan.players_per_flop, 30)
        self.assertEqual(self.gotha.last_scan.unique_player_count, 3)
        self.assertEqual(self.gotha.last_scan.entry_count, 6)
        self.assertEqual(self.gotha.last_scan.one_tabler_count, 2)
        self.assertEqual(self.gotha.last_scan.two_tabler_count, 0)
        self.assertEqual(self.gotha.last_scan.three_tabler_count, 0)
        self.assertEqual(self.gotha.last_scan.four_tabler_count, 1)
        self.assertAlmostEqual(self.gotha.one_tabler_percent, 66.6, delta=0.1)
        self.assertAlmostEqual(self.gotha.two_tabler_percent, 0, delta=0.1)
        self.assertAlmostEqual(self.gotha.three_tabler_percent, 0, delta=0.1)
        self.assertAlmostEqual(self.gotha.four_tabler_percent, 33.3, delta=0.1)

        self.assertEqual(self.gotha.mtr, 2)

        self.assertEqual(self.gotha.avg_pot, 25)
        self.assertEqual(self.gotha.avg_players_per_flop, 30)
        self.assertEqual(self.gotha.avg_unique_player_count, 3)
        self.assertEqual(self.gotha.avg_entry_count, 6)
        self.assertEqual(self.gotha.avg_mtr, 2)
        self.assertEqual(self.gotha.avg_one_tabler_count, 2)
        self.assertEqual(self.gotha.avg_two_tabler_count, 0)
        self.assertEqual(self.gotha.avg_three_tabler_count, 0)
        self.assertEqual(self.gotha.avg_four_tabler_count, 1)
        self.assertAlmostEqual(self.gotha.avg_one_tabler_percent, 66.6, delta=0.1)
        self.assertAlmostEqual(self.gotha.avg_two_tabler_percent, 0, delta=0.1)
        self.assertAlmostEqual(self.gotha.avg_three_tabler_percent, 0, delta=0.1)
        self.assertAlmostEqual(self.gotha.avg_four_tabler_percent, 33.3, delta=0.1)

        self.scan_two_days_before()

        self.assertEqual(self.gotha.last_scan.datetime, self.two_days_before)
        self.assertEqual(self.gotha.last_scan.player_count, 4)
        self.assertEqual(self.gotha.last_scan.average_pot, 20)

        self.assertEqual(self.gotha.avg_pot, 22.5)
        self.assertEqual(self.gotha.avg_players_per_flop, 25)
        self.assertEqual(self.gotha.avg_unique_player_count, 2.5)
        self.assertEqual(self.gotha.avg_entry_count, 5)
        self.assertEqual(self.gotha.avg_mtr, 2)

        self.scan_three_hours_before()

        self.assertEqual(self.gotha.last_scan.datetime, self.three_hours_before)
        self.assertEqual(self.gotha.last_scan.player_count, 12)
        self.assertEqual(self.gotha.last_scan.average_pot, 30)

        self.assertAlmostEqual(self.gotha.avg_pot, 25, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_players_per_flop, 25, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_unique_player_count, 3, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_entry_count, 7.33, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_mtr, 2.44, delta=0.01)

        self.scan_two_hours_before()

        self.assertEqual(self.gotha.last_scan.datetime, self.two_hours_before)
        self.assertEqual(self.gotha.last_scan.player_count, 11)
        self.assertEqual(self.gotha.last_scan.average_pot, 35)

        self.assertAlmostEqual(self.gotha.avg_pot, 27.5, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_players_per_flop, 25.75, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_unique_player_count, 3.25, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_entry_count, 8.25, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_mtr, 2.538, delta=0.01)

        self.scan_one_hour_before()

        self.assertEqual(self.gotha.last_scan.datetime, self.one_hour_before)
        self.assertEqual(self.gotha.last_scan.player_count, 10)
        self.assertEqual(self.gotha.last_scan.average_pot, 26)

        self.assertAlmostEqual(self.gotha.avg_pot, 27.2, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_players_per_flop, 25.4, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_unique_player_count, 3.2, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_entry_count, 8.6, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_mtr, 2.6875, delta=0.01)

        self.scan_now()

        self.assertEqual(self.gotha.last_scan.datetime, self.now)
        self.assertEqual(self.gotha.last_scan.player_count, 13)
        self.assertEqual(self.gotha.last_scan.average_pot, 29)
        self.assertAlmostEqual(self.gotha.one_tabler_percent, 40, delta=0.1)
        self.assertAlmostEqual(self.gotha.two_tabler_percent, 0, delta=0.1)
        self.assertAlmostEqual(self.gotha.three_tabler_percent, 20, delta=0.1)
        self.assertAlmostEqual(self.gotha.four_tabler_percent, 40, delta=0.1)

        self.assertAlmostEqual(self.gotha.avg_pot, 27.5, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_players_per_flop, 25.5, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_unique_player_count, 3.5, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_entry_count, 9.33, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_mtr, 2.66, delta=0.01)

        self.assertAlmostEqual(self.gotha.avg_one_tabler_count, 1.16, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_two_tabler_count, 0.33, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_three_tabler_count, 0.5, delta=0.01)
        self.assertAlmostEqual(self.gotha.avg_four_tabler_count, 1.5, delta=0.01)

        self.assertAlmostEqual(self.gotha.avg_one_tabler_percent, 33.3, delta=0.1)
        self.assertAlmostEqual(self.gotha.avg_two_tabler_percent, 9.5, delta=0.1)
        self.assertAlmostEqual(self.gotha.avg_three_tabler_percent, 14.3, delta=0.1)
        self.assertAlmostEqual(self.gotha.avg_four_tabler_percent, 42.9, delta=0.1)

        self.assertEqual(self.gotha._chart('average_pot', LAST_24)['values'],
                         [30, 35, 26, 29])
        self.assertEqual(self.gotha._chart('players_per_flop', LAST_24)['values'],
                         [25, 28, 24, 26])
        self.assertEqual(self.gotha._chart('one_tabler_count', LAST_24)['values'],
                         [1, 1, 0, 2])


        chart_values = self.gotha._chart('average_pot', BY_HOUR)['values']
        chart_times = self.gotha._chart('average_pot', BY_HOUR)['dates']
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 24.66, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 26, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 35, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 30, delta=0.1)

        chart_values = self.gotha._chart('one_tabler_count', BY_HOUR)['values']
        chart_times = self.gotha._chart('one_tabler_count', BY_HOUR)['dates']
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 1.66, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 1, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 1, delta=0.1)

        chart_values = self.gotha._chart('one_tabler_percent', BY_HOUR)['values']
        chart_times = self.gotha._chart('one_tabler_percent', BY_HOUR)['dates']
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 25, delta=0.1)

        chart_values = self.gotha._chart('two_tabler_percent', BY_HOUR)['values']
        chart_times = self.gotha._chart('two_tabler_percent', BY_HOUR)['dates']
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 25, delta=0.1)

        chart_values = self.gotha._chart('three_tabler_percent', BY_HOUR)['values']
        chart_times = self.gotha._chart('three_tabler_percent', BY_HOUR)['dates']
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 25, delta=0.1)

        chart_values = self.gotha._chart('four_tabler_percent', BY_HOUR)['values']
        chart_times = self.gotha._chart('four_tabler_percent', BY_HOUR)['dates']
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 25, delta=0.1)

        chart_values = self.gotha._chart('one_tabler_percent', LAST_24)['values']
        self.assertAlmostEqual(chart_values[0], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 40, delta=0.1)

        chart_values = self.gotha._chart('two_tabler_percent', LAST_24)['values']
        self.assertAlmostEqual(chart_values[0], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 33.3, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 0, delta=0.1)

        chart_values = self.gotha._chart('three_tabler_percent', LAST_24)['values']
        self.assertAlmostEqual(chart_values[0], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 20, delta=0.1)

        chart_values = self.gotha._chart('four_tabler_percent', LAST_24)['values']
        self.assertAlmostEqual(chart_values[0], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 66.6, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 40, delta=0.1)
