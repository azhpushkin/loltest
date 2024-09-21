from django.urls import path

from .views import HomeView, RaceView, JSView, LatestRequest, SettingsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('race/<race_id>', RaceView.as_view(), name='race'),
    path('js/<race_id>', JSView.as_view(content_type='text/javascript'), name='js'),

    path('race/<race_id>/latest', LatestRequest.as_view(), name='latest'),
    path('race/<race_id>/settings', SettingsView.as_view(), name='settings'),
    # path('race/<race_id>/latest', LatestRequest.as_view(), name='latest'),
]