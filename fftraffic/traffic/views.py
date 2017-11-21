from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Table
# Create your views here.


def index(request):
    tables = Table.objects.all()
    scanned_tables = [table.last_scan for table in tables if table.last_scan]
    context = {'table_scans': scanned_tables}
    template = 'traffic/index.html'
    return render(request, template, context)


def table(request, room, table_name):
    pass


@api_view(['PUT'])
def update_scans(request):
    if request.method == 'PUT':
        return Response({})
