from django.contrib import admin
from .models import Player, Table, Scanner, Scan, TableScan, Country

# Register your models here.


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'limit', 'max_players', 'last_table_scan_datetime', 'last_scan_datetime')

    @staticmethod
    def last_table_scan_datetime(table):
        return '{:%Y-%m-%d %H-%M-%S}'.format(table.last_scan.datetime)

    @staticmethod
    def last_scan_datetime(table):
        return '{:%Y-%m-%d %H-%M-%S}'.format(table.last_scan.scan.start_datetime)


class TableScanAdmin(admin.ModelAdmin):
    list_display = ('table', 'datetime')


admin.site.register(Player)
admin.site.register(Table, TableAdmin)
admin.site.register(TableScan, TableScanAdmin)
admin.site.register(Scanner)
admin.site.register(Scan)
admin.site.register(Country)




