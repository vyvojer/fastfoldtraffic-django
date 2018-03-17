from datetime import timedelta
import re

from django.utils import timezone
import pygal

from .models import *

LAST_24 = 0
BY_HOUR = 1
BY_WEEKDAY = 2


class Charts:

    def __init__(self, table: Table) -> None:
        self.table = table

    def __getattr__(self, name: str):
        if "_chart_" in name:
            match = re.match(r'(.*)_chart_(.*)', name)
            if match:
                field = match.group(1)
                chart_type = match.group(2)
                if chart_type not in ('spark', 'last_24', 'by_hour', 'by_weekday'):
                    raise AttributeError('Bad chart_type "{}" in attribute "{}"'.format(chart_type, name))
                else:
                    if chart_type == 'spark':
                        data, _ = self._chart(field, LAST_24)
                        return self._render_spark_chart(data)
                    elif chart_type == 'last_24':
                        _, data = self._chart(field, LAST_24)
                        return self._render_line_chart(data)
                    else:
                        return self._chart(field, eval('{}'.format(chart_type)))[0]
            else:
                raise AttributeError("name")
        else:
            return super().__getattribute__(name)

    @staticmethod
    def _render_spark_chart(data: dict, title=None):
        spark_options = dict(
            fill=True,
            width=100,
            height=20,
            show_dots=False,
            show_legend=False,
            show_x_labels=False,
            show_y_labels=False,
            spacing=0,
            margin=0,
            min_scale=1,
            max_scale=2,
            explicit_size=True,
            no_data_text='',
            js=(),
        )
        chart = pygal.Line(**spark_options)
        values = data['values']
        chart.add(title, values)
        return chart.render(is_unicode=True)

    @staticmethod
    def _render_line_chart(data: list, title=None):
        options = dict(
            show_dots=False,
        )
        chart = pygal.DateTimeLine(**options)
        chart.x_label_rotation = 60
        chart.x_labels_major_count = 10
        chart.x_value_formatter = lambda dt: dt.strftime('%H:%M')
        chart.show_minor_x_labels = False
        chart.add(title, data)
        return chart.render(is_unicode=True)

    def _chart(self, field, chart_type):
        chart = {}
        if chart_type == LAST_24:
            if not hasattr(self, '_last_24'):
                self._last_24 = self.table.table_scans.filter(
                    datetime__gte=timezone.now() - timedelta(hours=24)).values()
            query_set = self._last_24
        elif chart_type == BY_HOUR:
            if not hasattr(self, '_by_hour'):
                self._by_hour = self.table.table_scans.by_hour().all()
            query_set = self._by_hour
        else:
            if not hasattr(self, '_by_weekday'):
                self._by_weekday = self.table.table_scans.by_weekday().all()
            query_set = self._by_weekday

        # Chart tuple consist of datetime and value
        if field == 'mtr':
            chart_tuples = [(table_scan['datetime'], table_scan['entry_count'] / table_scan['unique_player_count'])
                            for table_scan in query_set]
        elif '_percent' in field:
            count_field = field.replace('percent', 'count')
            if 'avg' in field:
                total_field = 'avg_unique_player_count'
            else:
                total_field = 'unique_player_count'
            chart_tuples = [(table_scan['datetime'],
                             table_scan[count_field]/table_scan[total_field] * 100) for table_scan in query_set]
        else:
            chart_tuples = [(table_scan['datetime'], table_scan[field]) for table_scan in query_set]

        chart_tuples.sort(key=lambda x: x[0])
        chart['values'] = [table_scan[1] for table_scan in chart_tuples]
        chart['dates'] = [table_scan[0] for table_scan in chart_tuples]
        return chart, chart_tuples
