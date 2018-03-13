from django.contrib import admin
from .models import Player, Table, Scanner, Scan, TableScan, Country

# Register your models here.


class TableAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'scan_count',
                    'avg_pot_',
                    'avg_players_per_flop_',
                    'avg_mtr_',
                    'last_scan_datetime')

    @staticmethod
    def last_scan_datetime(table):
        return '{:%Y-%m-%d %H-%M-%S}'.format(table.last_scan.scan.start_datetime)

    @staticmethod
    def avg_pot_(table):
        return '{:.2f}'.format(table.avg_pot)

    @staticmethod
    def avg_players_per_flop_(table):
        return '{:.2f}'.format(table.avg_players_per_flop)

    @staticmethod
    def avg_mtr_(table):
        return '{:.2f}'.format(table.avg_mtr)


class TableScanAdmin(admin.ModelAdmin):
    list_display = ('table', 'datetime')


admin.site.register(Player)
admin.site.register(Table, TableAdmin)
admin.site.register(TableScan, TableScanAdmin)
admin.site.register(Scanner)
admin.site.register(Scan)
admin.site.register(Country)




