from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.

LAST_24 = 0
BY_HOUR = 1
BY_WEEKDAY = 2

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
        return self.table_scans.latest('datetime')

    @property
    def mtr(self):
        """ Multitable ratio"""
        try:
            mtr = self.last_scan.entry_count / self.last_scan.unique_player_count
        except ZeroDivisionError:
            mtr = 0
        return mtr

    @property
    def scan_count(self):
        """ Total number of scan """
        return self.table_scans.count()

    @property
    def avg_pot(self):
        avg_pot = self.table_scans.filter(average_pot__gt=0).aggregate(models.Avg('average_pot'))['average_pot__avg']
        if avg_pot:
            return avg_pot
        else:
            return 0

    @property
    def avg_players_per_flop(self):
        avg_players_per_flop = self.table_scans.filter(
            players_per_flop__gt=0).aggregate(models.Avg('players_per_flop'))['players_per_flop__avg']
        if avg_players_per_flop:
            return avg_players_per_flop
        else:
            return 0

    @property
    def avg_entry_count(self):
        avg_entry_count = self.table_scans.aggregate(models.Avg('entry_count'))['entry_count__avg']
        if avg_entry_count:
            return avg_entry_count
        else:
            return 0

    @property
    def avg_unique_player_count(self):
        avg_unique_player_count = self.table_scans.aggregate(models.Avg('unique_player_count'))[
            'unique_player_count__avg']
        if avg_unique_player_count:
            return avg_unique_player_count
        else:
            return 0

    @property
    def avg_mtr(self):
        e = self.table_scans.aggregate(models.Sum('entry_count'))['entry_count__sum']
        p = self.table_scans.aggregate(models.Sum('unique_player_count'))['unique_player_count__sum']
        if e and p:
            return e / p
        else:
            return 0

    @property
    def avg_one_tabler_count(self):
        avg_one_tabler_count = self.table_scans.aggregate(models.Avg('one_tabler_count'))[
            'one_tabler_count__avg']
        if avg_one_tabler_count:
            return avg_one_tabler_count
        else:
            return 0

    @property
    def avg_two_tabler_count(self):
        avg_two_tabler_count = self.table_scans.aggregate(models.Avg('two_tabler_count'))[
            'two_tabler_count__avg']
        if avg_two_tabler_count:
            return avg_two_tabler_count
        else:
            return 0

    @property
    def avg_three_tabler_count(self):
        avg_three_tabler_count = self.table_scans.aggregate(models.Avg('three_tabler_count'))[
            'three_tabler_count__avg']
        if avg_three_tabler_count:
            return avg_three_tabler_count
        else:
            return 0

    @property
    def avg_four_tabler_count(self):
        avg_four_tabler_count = self.table_scans.aggregate(models.Avg('four_tabler_count'))[
            'four_tabler_count__avg']
        if avg_four_tabler_count:
            return avg_four_tabler_count
        else:
            return 0

    def chart(self, field, chart_type):
        chart = {}
        if chart_type == LAST_24:
            if not hasattr(self, '_last_24'):
                self._last_24 = self.table_scans.filter(
                    datetime__gte=timezone.now() - timedelta(hours=24)).values()
            query_set = self._last_24
        if chart_type == BY_HOUR:
            if not hasattr(self, '_by_hour'):
                self._by_hour = self.table_scans.by_hour().all()
            query_set = self._by_hour

        if field == 'mtr':
            chart_tuples = [(table_scan['datetime'], table_scan['entry_count'] / table_scan['unique_player_count'])
                            for table_scan in query_set]
        else:
            chart_tuples = [(table_scan['datetime'], table_scan[field]) for table_scan in query_set]

        chart_tuples.sort(key=lambda x: x[0])
        chart['values'] = [table_scan[1] for table_scan in chart_tuples]
        chart['dates'] = [table_scan[0] for table_scan in chart_tuples]
        return chart


class Scanner(models.Model):
    name = models.CharField(max_length=20, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class Scan(models.Model):
    scanner = models.ForeignKey(Scanner, related_name='scans', on_delete=models.CASCADE)
    full = models.BooleanField(default=True)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)
    room = models.CharField(max_length=3, choices=ROOMS, default=ROOMS[0][0])

    def __str__(self):
        return "{} {:%Y-%m-%d %H-%M-%S}".format(self.scanner, self.end_datetime)


class TableScanQueryset(models.QuerySet):

    def by_hour(self):
        return self._extra("EXTRACT(HOUR FROM datetime)", 'datetime')

    def by_weekday(self):
        return self._extra("EXTRACT(HOUR FROM datetime)", 'datetime')

    def _extra(self, extra_clause, extra_name='datetime'):
        query_set = self.extra({extra_name: extra_clause}).values(extra_name).annotate(
            average_pot=models.Avg('average_pot'),
            players_per_flop=models.Avg('players_per_flop'),
            unique_player_count=models.Avg('unique_player_count'),
            one_tabler_count=models.Avg('one_tabler_count'),
            two_tabler_count=models.Avg('two_tabler_count'),
            three_tabler_count=models.Avg('three_tabler_count'),
            four_tabler_count=models.Avg('four_tabler_count'),

        )
        return query_set


class TableScan(models.Model):
    scan = models.ForeignKey(Scan, related_name='table_scans', on_delete=models.CASCADE)
    table = models.ForeignKey(Table, related_name='table_scans', on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, blank=True, db_index=True)
    player_count = models.SmallIntegerField(default=0)
    average_pot = models.FloatField(default=0.0)
    players_per_flop = models.SmallIntegerField(default=0)
    unique_player_count = models.SmallIntegerField(default=0)
    entry_count = models.SmallIntegerField(default=0)
    one_tabler_count = models.SmallIntegerField(default=0)
    two_tabler_count = models.SmallIntegerField(default=0)
    three_tabler_count = models.SmallIntegerField(default=0)
    four_tabler_count = models.SmallIntegerField(default=0)

    objects = TableScanQueryset.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=['datetime']),
        ]

    def __str__(self):
        return "{} players={} {:%Y-%m-%d %H-%M-%S}/{:%Y-%m-%d %H-%M-%S}".format(self.table,
                                                                                self.player_count,
                                                                                self.datetime,
                                                                                self.scan.end_datetime)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.one_tabler_count = self.players.filter(entries=1).count()
        self.two_tabler_count = self.players.filter(entries=2).count()
        self.three_tabler_count = self.players.filter(entries=3).count()
        self.four_tabler_count = self.players.filter(entries=4).count()
        super().save(force_insert, force_update, using, update_fields)


class PlayerScan(models.Model):
    player = models.ForeignKey(Player, related_name='scans', on_delete=models.CASCADE)
    table_scan = models.ForeignKey(TableScan, related_name='players', on_delete=models.CASCADE)
    entries = models.SmallIntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=['entries']),
        ]

    def __str__(self):
        return "{} entries={}".format(self.player, self.entries)
