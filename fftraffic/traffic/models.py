from django.db import models

# Create your models here.

ROOMS = (
    ('PS', 'PokerStars'),
)

GAMES = (
    ('NL', "NL Hold'em"),
    ('PLO', "PL Omaha"),
    ('PLO8', "PL Omaha H/L"),
    ('NLO8', "NL Omaha H/L"),
)


class Country(models.Model):
    iso = models.CharField(unique=True, max_length=2)
    name = models.CharField(default='', max_length=20)

    def __str__(self):
        return self.name


class Player(models.Model):
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])
    name = models.CharField(max_length=15)
    country = models.ForeignKey(Country)

    class Meta:
        unique_together = ('room', 'name')

    def __str__(self):
        return "{} ({})".format(self.name, self.country)


class Table(models.Model):
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])
    name = models.CharField(max_length=15)
    game = models.CharField(max_length=4, choices=GAMES, default=GAMES[0][0])
    limit = models.IntegerField(default=0)

    class Meta:
        unique_together = ('room', 'name')

    def __str__(self):
        return "{} ({} {})".format(self.name, self.game, self.limit)

    @property
    def last_scan(self):
        return self.scans.last()


class Scanner(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{}".format(self.ip)


class Scan(models.Model):
    scanner = models.ForeignKey(Scanner, related_name='scans')
    datetime = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])

    def __str__(self):
        return "{} {}".format(self.scanner, self.datetime)


class TableScan(models.Model):
    scan = models.ForeignKey(Scan, related_name='tables')
    table = models.ForeignKey(Table, related_name='scans')
    player_count = models.SmallIntegerField(default=0)
    average_pot = models.FloatField(default=0.0)
    players_per_flop = models.SmallIntegerField(default=0)
    hands_per_hour = models.SmallIntegerField(default=0)
    unique_player_count = models.SmallIntegerField(default=0)
    entry_count = models.SmallIntegerField(default=0)

    def __str__(self):
        return "{} players={}".format(self.table, self.player_count)


class PlayerScan(models.Model):
    player = models.ForeignKey(Player, related_name='scans')
    table_scan = models.ForeignKey(TableScan, related_name='players')
    entries = models.SmallIntegerField(default=1)

    def __str__(self):
        return "{} entries={}".format(self.player, self.entries)


