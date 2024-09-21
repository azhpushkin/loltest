from django.http import HttpResponse
from .models import *
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404




class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        races = Race.object.order_by('is_active')
        return {
            'races': races
        }

class RaceView(TemplateView):
    template_name = 'race.html'

    def get_context_data(self, race_id, **kwargs):
        race = get_object_or_404(race_id)
        
        return {
            'race': race
        }

class JSView(TemplateView):
    template_name = 'apex.js'

    def get_context_data(self, race_id, **kwargs):
        race = get_object_or_404(race_id)
        
        return {
            'race': race
        }
