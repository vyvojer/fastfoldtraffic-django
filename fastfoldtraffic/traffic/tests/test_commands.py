from datetime import timedelta

from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User
from django.utils import timezone

from traffic.allowed import ALLOWED_TABLES, ALLOWED_COUNTRIES
from traffic.models import Table, Country, Player, Scan, Scanner, TableScan


class PopulateTest(TestCase):

    def test_empty_tables(self):
        """ Populate empty table"""
        management.call_command('populate')
        tables = Table.objects.all()
        self.assertEqual(len(tables), len(ALLOWED_TABLES))

    def test_not_empty_tables(self):
        """ Tables table already having some tables"""
        Table.objects.create(room='PS', name='Arp')
        Table.objects.create(room='PS', name='Gotha')
        tables = Table.objects.all()
        self.assertEqual(len(tables), 2)
        arp = Table.objects.get(room='PS', name='Arp')
        gotha = Table.objects.get(room='PS', name='Gotha')
        self.assertEqual(arp.game, 'NL')
        self.assertEqual(arp.limit, 0)
        self.assertEqual(arp.max_players, 6)
        self.assertEqual(gotha.game, 'NL')
        self.assertEqual(gotha.limit, 0)
        self.assertEqual(gotha.max_players, 6)

        management.call_command('populate')
        tables = Table.objects.all()
        self.assertEqual(len(tables), len(ALLOWED_TABLES))

        arp = Table.objects.get(room='PS', name='Arp')
        self.assertEqual(arp.game, 'NL')
        self.assertEqual(arp.limit, 50)
        self.assertEqual(arp.max_players, 9)

        gotha = Table.objects.get(room='PS', name='Gotha')
        self.assertEqual(gotha.game, 'PLO')
        self.assertEqual(gotha.limit, 100)
        self.assertEqual(gotha.max_players, 6)

    def test_empty_countries(self):
        """ Populate empty contries"""
        management.call_command('populate')
        countries = Country.objects.all()
        self.assertEqual(len(countries), len(ALLOWED_COUNTRIES))

    def test_users(self):
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        management.call_command('populate')
        users = User.objects.all()
        self.assertEqual(len(users), 2)
        management.call_command('populate')
        users = User.objects.all()
        self.assertEqual(len(users), 2)


class RepairDatetimeTest(TestCase):

    def setUp(self):
        self.now = timezone.now()
        self.old_time = self.now - timedelta(hours=8)
        self.albania = Country.objects.create(iso='AL', name='Albania')
        self.nigeria = Country.objects.create(iso='NI', name='Nigeria')
        self.pushkin = Player.objects.create(name='pushkin', country=self.nigeria)
        self.obama = Player.objects.create(name='obama', country=self.nigeria, room='PS')
        self.lenin = Player.objects.create(name='lenin', country=self.albania, room='PS')
        self.aquarium = Table.objects.create(name='Aquarium')
        self.kino = Table.objects.create(name='Kino')
        self.scanner = Scanner.objects.create(ip='192.168.0.1', name='main')
        self.scan_1 = Scan.objects.create(scanner=self.scanner, datetime=self.now)
        self.table_scan_0_aquarium = TableScan.objects.create(scan=self.scan_1,
                                                              table=self.aquarium,
                                                              player_count=2)
        self.table_scan_0_kino = TableScan.objects.create(scan=self.scan_1,
                                                          table=self.kino,
                                                          player_count=2,
                                                          datetime=self.old_time)

    def testRepair(self):
        table_scans = TableScan.objects.all().order_by('table__name')
        self.assertNotEqual(table_scans[0].datetime, self.now)
        self.assertEqual(table_scans[1].datetime, self.old_time)
        management.call_command('repair_datetime')
        table_scans = TableScan.objects.all().order_by('table__name')
        self.assertEqual(table_scans[0].datetime, self.now)
        self.assertEqual(table_scans[1].datetime, self.old_time)



