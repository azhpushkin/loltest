
import logging
import time
from typing import Optional
from django.utils import timezone


import django

django.setup()  # noqa


from core.models import Race, BoardRequest  # noqa

from websockets.sync.client import connect

logger = logging.getLogger(__name__)

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'


def query(race):
    message = get_message(race.wss_url)

    if not message:
        return 
    
    try:
        br = BoardRequest(
            race=race,
            url=race.wss_url,
            created_at=timezone.now(),
            response_status=200,
            response_body=message
        )
        br.save()
    except Exception as ex:
        logger.error("Error on request save: " + str(ex))
        




def get_message(url):
    try:
        with connect(url, user_agent_header=USER_AGENT) as ws:
            message = ws.recv()
        
        return message
    except Exception as ex:
        logger.error("Error on ws receive: " + str(ex))
        return None

# DJANGO_SETTINGS_MODULE=timings.settings python -m processing

if __name__ == '__main__':
    logger.info('Starting worker')
    current_race: Optional[Race] = None
    while True:
        if not current_race:
            current_race = Race.objects.filter(is_active=True).first()
            if current_race:
                logger.info('New active race found', extra={'race': current_race.id})
            else:
                logger.info('No active race, waiting')
                time.sleep(3)
                continue
        
        current_race.refresh_from_db()
        if current_race.is_active:
            query(current_race)
            logger.info(
                'Race request processed', extra={'race': current_race.id}
            )
        else:
            logger.info('Race deactivated', extra={'race': current_race.id})
            current_race = None

        time.sleep(3)