import logging

from rest_framework import serializers

from .models import Scanner, Scan, Table, TableScan, Country, Player, PlayerScan
from .allowed import ALLOWED_TABLES as allowed_tables

logger = logging.getLogger('django')

allowed = {(table[0], table[1]) for table in allowed_tables}


class PlayerScanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15)
    country = serializers.CharField(max_length=2, allow_null=True)
    entries = serializers.IntegerField()


class TableScanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    player_count = serializers.IntegerField()
    average_pot = serializers.FloatField()
    players_per_flop = serializers.IntegerField()
    unique_player_count = serializers.IntegerField()
    entry_count = serializers.IntegerField()
    datetime = serializers.DateTimeField(allow_null=True)
    players = PlayerScanSerializer(many=True)


class ScanSerializer(serializers.Serializer):
    scanner_name = serializers.CharField(max_length=20)
    room = serializers.CharField(max_length=3)
    full = serializers.BooleanField()
    start_datetime = serializers.DateTimeField(allow_null=True)
    end_datetime = serializers.DateTimeField(allow_null=True)  #  use datetime.datetime.now().isoformat()
    tables = TableScanSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        tables_data = validated_data.pop('tables')
        scanner_name = validated_data.pop('scanner_name')
        room = validated_data.get('room')
        start_datetime = validated_data.pop('start_datetime')
        scanner, _ = Scanner.objects.get_or_create(name=scanner_name)
        scan, _ = Scan.objects.get_or_create(scanner=scanner, start_datetime=start_datetime)
        scan.end_datetime = validated_data.pop('end_datetime')
        scan.full = validated_data.pop('full')
        scan.save()
        for table_data in tables_data:
            players_data = table_data.pop('players')
            table_name = table_data.pop('name')
            if (room, table_name) not in allowed:
                logger.error("Attempt add not allowed table '{} {}'".format(room, table_name))
            else:
                table, _ = Table.objects.get_or_create(name=table_name)
                table_scan = TableScan.objects.create(scan=scan, table=table, **table_data)
                for player_data in players_data:
                    iso = player_data.pop('country')
                    if not iso:
                        iso = 'UC'
                    country, _ = Country.objects.get_or_create(iso=iso)
                    player_name = player_data.pop('name')
                    try:
                        player = Player.objects.get(room=room, name=player_name)
                    except Player.DoesNotExist:
                        player = Player.objects.create(room=room, name=player_name, country=country)
                    else:
                        if player.country.iso == 'UC' and iso:
                            player.country = country
                            player.save()

                    PlayerScan.objects.create(player=player, table_scan=table_scan, **player_data)

        logger.info("Scanner '%s' just uploaded info about %s tables", scanner_name, len(tables_data))




