from django.shortcuts import render
from .models import Table
# Create your views here.


def index(request):
    tables = Table.objects.all()
    scanned_tables = [table.last_scan for table in tables if table.last_scan]
    context = {'table_scans': scanned_tables}
    template = 'traffic/index.html'
    return render(request, template, context)
