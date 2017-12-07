from django.core.management.base import BaseCommand, CommandError
from traffic.models import Table
from traffic.allowed import ALLOWED_TABLES


class Command(BaseCommand):
    help = 'Populate tables and countries'

    def handle(self, *args, **options):
        for table_allowed in ALLOWED_TABLES:
            room = table_allowed[0]
            name = table_allowed[1]
            game = table_allowed[2]
            limit = table_allowed[3]
            table, _ = Table.objects.get_or_create(room=room, name=name)
            table.game = game
            table.limit = limit
            table.save()

