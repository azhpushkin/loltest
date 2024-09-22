from django.http import HttpResponse
from .models import *
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse




class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        races = Race.objects.order_by('is_active')
        return {
            'races': races
        }

class RaceView(TemplateView):
    template_name = 'race.html'

    def get_context_data(self, race_id, **kwargs):
        race = get_object_or_404(Race, id=race_id)
        
        return {
            'race': race
        }
    

class SettingsView(TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, race_id, **kwargs):
        race = get_object_or_404(Race, id=race_id)
        
        return {
            'race': race
        }


class JSView(TemplateView):
    template_name = 'apex.js'

    def get_context_data(self, race_id, **kwargs):
        race = get_object_or_404(Race, id=race_id)
        
        return {
            'race': race,
        }
    
class LatestRequest(View):
    def get(self, *args, **kwargs):
        race_id = kwargs['race_id']
        br = BoardRequest.objects.filter(race_id=race_id).order_by('-created_at').first()
        if not br:
            return HttpResponse('')
        else:
            return HttpResponse(br.response_body)


class GetLast10Minutes(View):
    def get(self, *args, **kwargs):
        race_id = kwargs['race_id']
        brs = BoardRequest.objects.order_by('created_at')
        data = [{
            'data': br.response_body
        } for br in brs]
        print(type(brs[0].response_body))
        return JsonResponse({'requests': data})
