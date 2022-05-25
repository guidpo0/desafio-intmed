from django.contrib import admin
from medicar import models


class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'crm')
    list_display_links = ('id', 'nome')


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'medico', 'dia')
    list_display_links = ('id', 'medico')


admin.site.register(models.Medico, MedicoAdmin)
admin.site.register(models.Agenda, AgendaAdmin)
