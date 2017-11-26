from django.shortcuts import render
from django.views import generic

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Table
from .serializers import ScanSerializer
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'traffic/index.html'
    context_object_name = 'tables'

    def get_queryset(self):
        """ Return the tables, that have scans """
        return Table.objects.filter(scans__isnull=False)


def table(request, room, table_name):
    pass


@api_view(['PUT'])
def update_scans(request):
    if request.method == 'PUT':
        scan_serializer = ScanSerializer(data=request.data)
        if scan_serializer.is_valid():
            scan_serializer.update(None, scan_serializer.data)
            return Response(scan_serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(scan_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
