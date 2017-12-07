from django.test import TestCase
from django.core import management

from traffic.allowed import ALLOWED_TABLES
from traffic.models import Table


class PrepopulateTest(TestCase):

    def test_empty_base(self):
        management.call_command('populate')
        tables = Table.objects.all()
        self.assertEqual(len(tables), len(ALLOWED_TABLES))

