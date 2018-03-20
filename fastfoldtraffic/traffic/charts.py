from datetime import timedelta
import re

import pygal

from .models import *

LAST_24 = 0
BY_HOUR = 1
BY_WEEKDAY = 2

_CHARTS = {}
_FIELDS = {}


class _Field:
    def __init__(self, db_field: str, label: str):
        self.db_field = db_field
        self.label = label

    def __str__(self):
        return self.db_field


class _Chart:
    def __init__(self, title: str, fields: list):
        self.title = title
        self.fields = list(fields)

    def __str__(self):
        return self.title


def _init():
    global _FIELDS
    global _CHARTS
    _FIELDS = {
        'unique_player_count': _Field('unique_player_count', 'Player Count'),
        'entry_count': _Field('entry_count', 'Entry Count'),
        'mtr': _Field('mtr', 'MTR'),
        'one_tabler_percent': _Field('one_tabler_percent', 'One-tablers (%)'),
        'two_tabler_percent': _Field('two_tabler_percent', 'Two-tablers (%)'),
        'three_tabler_percent': _Field('three_tabler_percent', 'Three-tablers (%)'),
        'four_tabler_percent': _Field('four_tabler_percent', 'Four-tablers (%)'),
        'average_pot': _Field('average_pot', 'Average Pot'),
        'players_per_flop': _Field('players_per_flop', 'Players Per Flop'),

    }
    _CHARTS = {
        'unique_player_count': _Chart("Player Count", fields=[_FIELDS['unique_player_count']]),
        'entry_count': _Chart("Entry Count", fields=[_FIELDS['entry_count']]),
        'player_count': _Chart("Players", fields=[_FIELDS['entry_count'], _FIELDS['unique_player_count']]),
        'mtr': _Chart("Multi Table Ratio", fields=[_FIELDS['mtr']]),
        'one_tabler_percent': _Chart("One-tabler Percent", fields=[_FIELDS['one_tabler_percent']]),
        'two_tabler_percent': _Chart("One-tabler Percent", fields=[_FIELDS['two_tabler_percent']]),
        'three_tabler_percent': _Chart("One-tabler Percent", fields=[_FIELDS['three_tabler_percent']]),
        'four_tabler_percent': _Chart("One-tabler Percent", fields=[_FIELDS['four_tabler_percent']]),
        'average_pot': _Chart("Average Pot", fields=[_FIELDS['average_pot']]),
        'players_per_flop': _Chart("Players Per Flop", fields=[_FIELDS['players_per_flop']]),
    }


_init()


class Charts:

    def __init__(self, table: Table) -> None:
        self.table = table
        self._last_24 = None
        self._by_hour = None
        self._by_weekday = None

    def __getattr__(self, name: str):
        if "_chart_" in name:
            match = re.match(r'(.*)_chart_(.*)', name)
            if match:
                chart_key = match.group(1)
                chart_type = match.group(2)
                if chart_type not in ('spark', 'last_24', 'by_hour', 'by_weekday'):
                    raise AttributeError('Bad chart_type "{}" in attribute "{}"'.format(chart_type, name))
                else:
                    chart = _CHARTS[chart_key]
                    fields, datas = self._get_data_for_chart(chart, chart_type)
                    return self._render_chart(chart, chart_type, fields, datas)
            else:
                raise AttributeError("name")
        else:
            return super().__getattribute__(name)

    def _get_data_for_chart(self, chart: _Chart, chart_type) -> (list, list):
        fields = []
        datas = []
        for field in chart.fields:
            if chart_type in ['spark', 'last_24']:
                chart_data = self._get_chart_data(field.db_field, LAST_24)
            elif chart_type == 'by_hour':
                chart_data = self._get_chart_data(field.db_field, BY_HOUR)
            else:
                chart_data = self._get_chart_data(field.db_field, BY_WEEKDAY)
            fields.append(field)
            datas.append(chart_data)
        return fields, datas

    @staticmethod
    def _render_chart(chart: _Chart, chart_type: str, fields: list, datas: list):
        options = {}

        if chart.title == "Multi-tablers":
            pyg_chart = pygal.StackedLine()
        elif chart_type in ['spark', 'last_24']:
            pyg_chart = pygal.DateTimeLine()
        else:
            pyg_chart = pygal.Bar()

        if chart_type == 'spark':
            pyg_chart.fill = True
            pyg_chart.width = 100
            pyg_chart.height = 20
            pyg_chart.show_dots = False
            pyg_chart.show_legend = False
            pyg_chart.show_x_labels = False
            pyg_chart.show_y_labels = False
            pyg_chart.spacing = 0
            pyg_chart.margin = 0
            pyg_chart.min_scale = 1
            pyg_chart.max_scale = 2
            pyg_chart.explicit_size = True
            pyg_chart.no_data_text = ''
            pyg_chart.js = ()
        elif chart_type == 'last_24':
            pyg_chart.title = chart.title
            pyg_chart.fill = True
            pyg_chart.show_dots = False
            pyg_chart.legend_at_bottom = True
            pyg_chart.show_x_guides = True
            pyg_chart.spacing = 20
            pyg_chart.margin = 20
            pyg_chart.x_label_rotation = 45
            pyg_chart.x_labels_major_count = 15
            pyg_chart.x_value_formatter = lambda dt: dt.strftime('%H:%M')
            pyg_chart.show_minor_x_labels = False
        elif chart_type == 'by_hour':
            pyg_chart.title = chart.title
            pyg_chart.x_labels = [value[0] for value in datas[0]]
        else:
            pyg_chart.title = chart.title
            pyg_chart.x_labels = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

        for field, data in zip(fields, datas):
            if chart_type in ['spark', 'last_24']:
                pyg_chart.add(field.label, data)
            else:
                pyg_chart.add(field.label, [value[1] for value in data])

        return pyg_chart.render(is_unicode=True)

    @property
    def last_24(self):
        if self._last_24 is None:
            self._last_24 = self.table.table_scans.filter(
                datetime__gte=timezone.now() - timedelta(hours=24)).values()
        return self._last_24

    @property
    def by_hour(self):
        if self._by_hour is None:
            self._by_hour = self.table.table_scans.by_hour().all()
        return self._by_hour

    @property
    def by_weekday(self):
        if self._by_weekday is None:
            self._by_weekday = self.table.table_scans.by_weekday().all()
        return self._by_weekday

    def _get_chart_data(self, field, chart_type):
        """ Return list of tuples (datatime, value)"""
        chart = {}
        if chart_type == LAST_24:
            query_set = self.last_24
        elif chart_type == BY_HOUR:
            query_set = self.by_hour
        else:
            query_set = self.by_weekday

        # Chart tuple consist of datetime and value
        if field == 'mtr':
            chart_data = [(table_scan['datetime'],
                           table_scan['entry_count'] / table_scan['unique_player_count'] if table_scan[
                               'unique_player_count'] else 0)
                          for table_scan in query_set]
        elif '_percent' in field:
            count_field = field.replace('percent', 'count')
            if 'avg' in field:
                total_field = 'avg_unique_player_count'
            else:
                total_field = 'unique_player_count'
            chart_data = [(table_scan['datetime'],
                           table_scan[count_field] / table_scan[total_field] * 100 if table_scan[total_field] else 0)
                          for table_scan in query_set]
        else:
            chart_data = [(table_scan['datetime'], table_scan[field]) for table_scan in query_set]

        chart_data.sort(key=lambda x: x[0])
        return chart_data
