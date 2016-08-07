import pygame.midi
import homeassistant.remote as remote
import random
from helpers import get_credentials

pygame.init()
pygame.fastevent.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
credentials = get_credentials()
api = remote.API(api_password=credentials['api_password'], port=443, use_ssl=True, host=credentials['host'])

domain = 'light'
arguments = {
    "entity_id": 'light.living_room',
    "color_temp": 375,
    "brightness": 107,
}


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


print("starting")
previous = None
going = True
i = pygame.midi.Input(input_id)
while going:

    if i.poll():
        midi_events = i.read(1)
        print(midi_events)
        v = translate(midi_events[0][0][1], 21, 108, 0, 0.8)
        if v == previous:
            continue
        previous = v
        if v != 64:
            print(v)
            arguments['xy_color'] = [random.uniform(0, 0.8), v]
            remote.call_service(api, domain, 'turn_on', arguments)

print("exit")
