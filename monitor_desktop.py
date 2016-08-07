from helpers import get_credentials
from time import sleep
import os, platform
import homeassistant.remote as remote
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)



def ping(host):
    """
    Returns True if host responds to a ping request
    """

    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    # Ping
    return 0 == os.system("ping " + ping_str + " " + host + "> /dev/null 2>&1")


def just_died(l):
    alives = sum(l)
    if alives > 3:
        return True

credentials = get_credentials()
api = remote.API(api_password=credentials['api_password'], port=443, use_ssl=True, host=credentials['host'])
previous = []
domain = 'light'
arguments = {
    "entity_id": 'light.desk',
    "color_temp": 375,
    "brightness": 107,
}

while True:
    alive = ping('192.168.0.60')
    desk = remote.get_state(api, 'light.desk')
    logger.debug('^^^^^^^^^^^')
    logger.debug("{previous} - {alive} - {state}".format(previous=previous, alive=alive, state=desk.state))

    if alive and desk.state == 'off':
        logger.info('alive and light is off, turning on')
        remote.call_service(api, domain, 'turn_on', arguments)
    if alive and desk.state == 'on':
        logger.debug('alive and light is on, pass')
        pass
    if not alive and desk.state == 'on':
        if just_died(previous):
            logger.info('just died and light is on, turning off')
            remote.call_service(api, domain, 'turn_off')
    if not alive and desk.state == 'off':
        logger.debug('not alive and light is off, pass')
        pass

    previous.append(alive)
    if len(previous) > 10:
        del previous[-1]
    sleep(3)
