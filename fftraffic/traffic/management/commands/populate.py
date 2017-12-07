from django.core.management.base import BaseCommand, CommandError
from traffic.models import Table, Country
from traffic.allowed import ALLOWED_TABLES, ALLOWED_COUNTRIES


class Command(BaseCommand):
    help = 'Populate tables and countries'

    def handle(self, *args, **options):
        for allowed_table in ALLOWED_TABLES:
            room = allowed_table[0]
            name = allowed_table[1]
            game = allowed_table[2]
            limit = allowed_table[3]
            max_players = allowed_table[4]
            table, _ = Table.objects.get_or_create(room=room, name=name)
            table.game = game
            table.limit = limit
            table.max_players = max_players
            table.save()

        for allowed_country in ALLOWED_COUNTRIES:
            name = allowed_country[0]
            iso = allowed_country[1]
            country, _ = Country.objects.get_or_create(iso=iso)
            country.name = name
            country.save()

