from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User

from traffic.allowed import ALLOWED_TABLES, ALLOWED_COUNTRIES
from traffic.models import Table, Country


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


