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
    name = models.CharField(default='', max_length=60)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'countries'

    def __str__(self):
        return "{} {}".format(self.iso, self.name)


class Player(models.Model):
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room', 'name')

    def __str__(self):
        return "{}".format(self.name)


class Table(models.Model):
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])
    name = models.CharField(max_length=15)
    game = models.CharField(max_length=4, choices=GAMES, default=GAMES[0][0])
    limit = models.IntegerField(default=0)
    max_players = models.IntegerField(default=6)

    class Meta:
        unique_together = ('room', 'name')
        ordering = ('room', 'game', 'max_players', 'limit',)

    def __str__(self):
        return "{} [{} {}] {} max".format(self.name, self.game, self.limit, self.max_players)

    def limit_str(self):
        if self.max_players != 6:
            max_str = '({}m)'.format(self.max_players)
        else:
            max_str = ''
        return "{} {} {}".format(self.game, self.limit, max_str)

    @property
    def last_scan(self):
        return self.scans.last()


class Scanner(models.Model):
    name = models.CharField(max_length=20, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class Scan(models.Model):
    scanner = models.ForeignKey(Scanner, related_name='scans', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])

    def __str__(self):
        return "{} {}".format(self.scanner, self.datetime)


class TableScan(models.Model):
    scan = models.ForeignKey(Scan, related_name='table_scans', on_delete=models.CASCADE)
    table = models.ForeignKey(Table, related_name='scans', on_delete=models.CASCADE)
    player_count = models.SmallIntegerField(default=0)
    average_pot = models.FloatField(default=0.0)
    players_per_flop = models.SmallIntegerField(default=0)
    unique_player_count = models.SmallIntegerField(default=0)
    entry_count = models.SmallIntegerField(default=0)

    def __str__(self):
        return "{} players={}".format(self.table, self.player_count)


class PlayerScan(models.Model):
    player = models.ForeignKey(Player, related_name='scans', on_delete=models.CASCADE)
    table_scan = models.ForeignKey(TableScan, related_name='players', on_delete=models.CASCADE)
    entries = models.SmallIntegerField(default=1)

    def __str__(self):
        return "{} entries={}".format(self.player, self.entries)


