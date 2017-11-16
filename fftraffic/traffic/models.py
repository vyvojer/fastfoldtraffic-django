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


class Scan(models.Model):
    pass


class TableScan(models.Model):
    pass


class PlayerScan(models.Model):
    pass


