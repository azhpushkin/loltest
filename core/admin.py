import io
import tempfile

import pandas as pd
from django.contrib import admin, messages
from django.db import connection
from django.http import HttpResponse

from core.models import Race, BoardRequest



@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'is_active')
    list_display_links = ('id', 'name')

@admin.register(BoardRequest)
class BoardRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'created_at',  'race_id', )
    list_per_page = 30

