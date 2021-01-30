'''
* Grupo 1363
* Pareja 8
* File: admin.py
'''

from django.contrib import admin
from datamodel.models import Game, Move


class GameAdmin(admin.ModelAdmin):
    list_display = ('id',)


class MoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'target')


admin.site.register(Game, GameAdmin)
admin.site.register(Move, MoveAdmin)
