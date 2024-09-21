from django.urls import path

from .views import HomeView, RaceView, JSView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('race/<race_id>', RaceView.as_view(), name='race'),
    path('js/<race_id>', JSView.as_view(), name='js'),
]