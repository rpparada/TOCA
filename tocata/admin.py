from django.contrib import admin
from .models import Tocata, TocataTicketFile

# Register your models here.


class TocataTicketFileInLine(admin.TabularInline):
    model = TocataTicketFile
    extra = 1

class TocataAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    inlines = [TocataTicketFileInLine]
    class Meta:
        model = Tocata

admin.site.register(Tocata, TocataAdmin)
