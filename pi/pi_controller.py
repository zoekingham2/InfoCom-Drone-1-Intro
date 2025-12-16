import requests
import time
import random
import click
from sense_hat import SenseHat

sense = SenseHat()
def get_direction():
    d_long = 0
    d_la = 0
    send_vel = False

    event = None
    while event is None:
        events = sense.stick.get_events()
        if events:
            event = events[0]

    if event.action in ["pressed", "held"]:
        if event.direction == "left":
            d_long = -1
            d_la = 0
            send_vel = True
        elif event.direction == "right":
            d_long = 1
            d_la = 0
            send_vel = True
        elif event.direction == "up":
            d_long = 0
            d_la = 1
            send_vel = True
        elif event.direction == "down":
            d_long = 0
            d_la = -1
            send_vel = True

    return d_long, d_la, send_vel



if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5000/drone"
    while True:
        d_long, d_la, send_vel = get_direction()
        if send_vel:
            with requests.Session() as session:
                current_location = {'longitude': d_long,
                                    'latitude': d_la
                                    }
                resp = session.post(SERVER_URL, json=current_location)
