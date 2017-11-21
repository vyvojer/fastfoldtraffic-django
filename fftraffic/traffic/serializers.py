from rest_framework import serializers

from .models import Table

class PlayerScanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15)
    country = serializers.CharField(max_length=2)
    entries = serializers.IntegerField()


class TableScanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    player_count = serializers.IntegerField()
    average_pot = serializers.FloatField()
    players_per_flop = serializers.IntegerField()
    hands_per_hour = serializers.IntegerField()
    unique_player_count = serializers.IntegerField()
    entry_count = serializers.IntegerField()
    players = PlayerScanSerializer(many=True)



class ScanSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=3)
    tables = TableScanSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

