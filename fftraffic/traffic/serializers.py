from rest_framework import serializers

from .models import Scanner, Scan, Table, TableScan, Country, Player, PlayerScan


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
    players = PlayerScanSerializer(many=True)


class ScanSerializer(serializers.Serializer):
    scanner_name = serializers.CharField(max_length=20)
    room = serializers.CharField(max_length=3)
    datetime = serializers.DateTimeField(allow_null=True)  #  use datetime.datetime.now().isoformat()
    tables = TableScanSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        tables_data = validated_data.pop('tables')
        scanner_name = validated_data.pop('scanner_name')
        room = validated_data.get('room')
        if validated_data.get('datetime') is None:
            validated_data.pot('datetime')
        scanner, _ = Scanner.objects.get_or_create(name=scanner_name)
        scan = Scan.objects.create(scanner=scanner, **validated_data)
        for table_data in tables_data:
            players_data = table_data.pop('players')
            table_name = table_data.pop('name')
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




