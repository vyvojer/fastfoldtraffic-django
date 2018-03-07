from django.core.management.base import BaseCommand

from traffic.models import TableScan, Scan


class Command(BaseCommand):

    help = 'Repaire TableScan.datatime (set to Scan.datetime if in future)'

    def handle(self, *args, **options):
        table_scans = TableScan.objects.all()
        for table_scan in table_scans:
            if table_scan.datetime > table_scan.scan.datetime:
                table_scan.datetime = table_scan.scan.datetime
                table_scan.save()