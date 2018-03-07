from django.contrib import admin
from .models import Player, Table, Scanner, Scan, TableScan, Country

# Register your models here.

class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'limit', 'last_scan')


class TableScanAdmin(admin.ModelAdmin):
    list_display = ('table', 'datetime')

admin.site.register(Player)
admin.site.register(Table, TableAdmin)
admin.site.register(TableScan, TableScanAdmin)
admin.site.register(Scanner)
admin.site.register(Scan)
admin.site.register(Country)




