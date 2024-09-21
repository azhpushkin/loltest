from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from django.core.exceptions import ValidationError


import requests
import re


class Race(models.Model):
    api_url = models.URLField(
        default='https://www.apex-timing.com/live-timing/kartcenter-campillos/'
    )
    config_port = models.IntegerField(blank=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                name='races_single_active',
                fields=['is_active'],
                condition=models.Q(is_active=True),
            )
        ]
        db_table = 'races'

    def clean(self):
        if not self.api_url.endswith('/'):
            self.api_url = self.api_url + '/'

        if not self.config_port:
            port, err = get_port(self.api_url)
            if err:
                raise ValidationError({
                    'config_port': ValidationError(err)
                })
            self.config_port = port
    
    @property
    def ws_url(self):
        p = self.config_port
        return f'ws://www.apex-timing.com:{p+2}/'
    
    @property
    def wss_url(self):
        p = self.config_port
        return f'wss://www.apex-timing.com:{p+3}/'
        
    def __str__(self):
        return f'<Race #{self.id} - {self.name}>'


class BoardRequest(models.Model):
    race = models.ForeignKey(Race, on_delete=models.PROTECT, verbose_name='requests')

    created_at = models.DateTimeField()
    url = models.TextField()

    response_status = models.IntegerField()
    response_body = models.TextField()

    class Meta:
        db_table = 'requests'


def get_port(url):
    port_re = re.compile(r'configPort = (?P<port>\d+);')

    try:
        resp = requests.get(url + '/javascript/config.js')
        if not str(resp.status_code).startswith('2'):
            return None, f'{resp}, {resp.content}'
        port = int(port_re.search(resp.text).group('port'))
        return port, None
    except Exception as ex:
        return None, str(ex)