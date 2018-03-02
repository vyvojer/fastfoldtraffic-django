from django.contrib import admin
from .models import Player, Table, Scanner, Scan, TableScan, Country

# Register your models here.

admin.site.register(Player)
admin.site.register(Table)
admin.site.register(TableScan)
admin.site.register(Scanner)
admin.site.register(Scan)
admin.site.register(Country)


