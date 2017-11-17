from django.db import models

# Create your models here.

POKER_ROOM = (
    ('PS', 'PokerStars'),
)

GAMES = (
    ('NL', "NL Hold'em"),
    ('PLO', "PL Omaha"),
    ('PLO8', "PL Omaha H/L"),
    ('NLO8', "NL Omaha H/L"),
)


class Country(models.Model):

    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Player(models.Model):

    room = models.CharField(max_length=3, choices=POKER_ROOM)
    name = models.CharField(max_length=15)
    country = models.OneToOneField(Country)

    class Meta:
        unique_together = ('room', 'name')

    def __str__(self):
        return "{} ({})".format(self.name, self.country)


class Table(models.Model):
    room = models.CharField(max_length=3, choices=POKER_ROOM)
    name = models.CharField(max_length=15)
    game = models.CharField(max_length=4, choices=GAMES)
    limit = models.IntegerField()

    class Meta:
        unique_together = ('room', 'name')

    def __str__(self):
        return "{} ({} {})".format(self.name, self.game, self.limit)


class Scanner(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    name = models.CharField(max_length=20)


class Scan(models.Model):
    scanner = models.ForeignKey(Scanner, related_name='scans')
    datetime = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=3, choices=POKER_ROOM)


class TableScan(models.Model):
    scan = models.ForeignKey(Scan)
    table = models.ForeignKey(Table)
    player_count = models.SmallIntegerField(default=0)
    average_pot = models.FloatField(default=0.0)
    players_per_flop = models.SmallIntegerField(default=0)
    hands_per_hour = models.SmallIntegerField(default=0)
    unique_player_count = models.SmallIntegerField(default=0)
    entry_count = models.SmallIntegerField(default=0)


class PlayerScan(models.Model):
    player = models.ForeignKey(Player)
    entries = models.SmallIntegerField()


