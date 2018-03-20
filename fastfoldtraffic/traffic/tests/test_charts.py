from datetime import timedelta

from django.test import TestCase
from traffic.models import *
from traffic.charts import *

class ChartTest(TestCase):

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

    def test_charts(self):
        self.scan_tree_days_before()
        self.scan_two_days_before()
        self.scan_three_hours_before()
        self.scan_two_hours_before()
        self.scan_one_hour_before()
        self.scan_now()

        charts = Charts(self.gotha)
        chart_values = [value[1] for value in charts._get_chart_data('average_pot', BY_HOUR)]
        chart_times = [value[0] for value in charts._get_chart_data('average_pot', BY_HOUR)]
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 24.66, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 26, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 35, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 30, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('one_tabler_count', BY_HOUR)]
        chart_times = [value[0] for value in charts._get_chart_data('one_tabler_count', BY_HOUR)]
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 1.66, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 1, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 1, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('one_tabler_percent', BY_HOUR)]
        chart_times = [value[0] for value in charts._get_chart_data('one_tabler_percent', BY_HOUR)]
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 25, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('two_tabler_percent', BY_HOUR)]
        chart_times = [value[0] for value in charts._get_chart_data('two_tabler_percent', BY_HOUR)]
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 33.3, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 0, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('three_tabler_percent', BY_HOUR)]
        chart_times = [value[0] for value in charts._get_chart_data('three_tabler_percent', BY_HOUR)]
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 20, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 25, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('four_tabler_percent', BY_HOUR)]
        chart_times = [value[0] for value in charts._get_chart_data('four_tabler_percent', BY_HOUR)]
        self.assertAlmostEqual(chart_values[chart_times.index(self.now.hour)], 30, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.one_hour_before.hour)], 66.6, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.two_hours_before.hour)], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[chart_times.index(self.three_hours_before.hour)], 50, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('one_tabler_percent', LAST_24)]
        self.assertAlmostEqual(chart_values[0], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 40, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('two_tabler_percent', LAST_24)]
        self.assertAlmostEqual(chart_values[0], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 33.3, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 0, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('three_tabler_percent', LAST_24)]
        self.assertAlmostEqual(chart_values[0], 25, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 0, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 20, delta=0.1)

        chart_values = [value[1] for value in charts._get_chart_data('four_tabler_percent', LAST_24)]
        self.assertAlmostEqual(chart_values[0], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[1], 50, delta=0.1)
        self.assertAlmostEqual(chart_values[2], 66.6, delta=0.1)
        self.assertAlmostEqual(chart_values[3], 40, delta=0.1)
