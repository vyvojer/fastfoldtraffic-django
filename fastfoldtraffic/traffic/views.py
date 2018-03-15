from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import pygal

from .models import Table, LAST_24
from .serializers import ScanSerializer


# Create your views here.


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


class IndexView(ListView):
    template_name = 'traffic/index.html'
    context_object_name = 'tables'

    def get_queryset(self):
        """ Return the tables, that have scans """

        return Table.objects.order_by('room', 'game', 'max_players', 'limit', )


class TableView(DetailView):
    model = Table
    context_object_name = 'table'
    template_name = 'traffic/table_general.html'

    def get_object(self, queryset=None):
        room = 'ps'
        name = self.kwargs['table_name'].replace('-', ' ')
        return get_object_or_404(Table, room__iexact=room, name__iexact=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = context['table']
        for field in [('unique_player_count', 'Players'),
                      ('entry_count', 'Entries'),
                      ('mtr', 'MTR'),
                      ('players_per_flop', 'Players Per Flop'),
                      ('average_pot', 'Average Pot'),
                      ]:
            context['{}_chart'.format(field[0])] = _render_spark_chart(table.chart(field[0], LAST_24), field[1])
        return context


@api_view(['PUT'])
def update_scans(request):
    if request.method == 'PUT':
        scan_serializer = ScanSerializer(data=request.data)
        if scan_serializer.is_valid():
            scan_serializer.update(None, scan_serializer.data)
            return Response(scan_serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            print(scan_serializer.errors)
            return Response(scan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
