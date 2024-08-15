from pynput import mouse, keyboard
from time import time
import json
import os

OUTPUT_FILENAME = 'actions'  # update to input from user later

mouse_listener = None  # Declaring globally so on_release can stop script

start_time = None  # Declare globally so that callback functions can reference

prev_x, prev_y = None, None

unreleased_keys = []  # keep track of unreleased keys

held_keys = set()

input_events = []  # store all input events


class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'
    MOVE = 'move'


def main(record_mouse_movements):
    runListeners(record_mouse_movements)
    print("Recording duration:{} seconds".format(elapsed_time()))
    global input_events
    print(json.dumps(input_events))

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, 'recordings', '{}.json'.format(OUTPUT_FILENAME))

    with open(filepath, 'w') as outfile:
        json.dump(input_events, outfile, indent=4)  # pretty up output


def elapsed_time():
    global start_time
    return time() - start_time


def record_event(event_type, event_time, button=None, pos=None):
    global input_events
    input_events.append({
        'time': event_time,
        'type': event_type,
        'button': str(button),  # handles button objects passed from pynput
        'pos': pos
    })

    if event_type == EventType.CLICK:
        print('{} on {} pos {} at {}'.format(event_type, button, pos, event_time))

    if event_type == EventType.MOVE:
        print('{} on {} pos {} at {}'.format(event_type, button, pos, event_time))

    else:
        print('{} on {} at {}'.format(event_type, button, event_time))


def on_press(key):
    # only record first key press event until release
    global unreleased_keys
    if key not in unreleased_keys:
        unreleased_keys.append(key)

    try:
        record_event(EventType.KEYDOWN, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYDOWN, elapsed_time(), key)


def on_release(key):
    # remove unreleased keys from list once released
    global unreleased_keys

    if key in unreleased_keys:
        try:
            record_event(EventType.KEYUP, elapsed_time(), key.char)
        except AttributeError:
            record_event(EventType.KEYUP, elapsed_time(), key)

    if key == keyboard.Key.esc:
        # Stop mouse listener
        global mouse_listener
        mouse_listener.stop()
        # Stop keyboard listener
        return False


def on_move(x, y,):
    global prev_x, prev_y

    if prev_x is None and prev_y is None:
        prev_x, prev_y = x, y

    rel_x, rel_y = x - prev_x, y - prev_y

    prev_x, prev_y = x, y

    record_event(EventType.MOVE, elapsed_time(), None, (rel_x, rel_y))


def on_click(x, y, button, pressed):
    # modified from documentation we are only using escape key
    if not pressed:
        record_event(EventType.CLICK, elapsed_time(), button, (x, y))


def runListeners(record_mouse_movements):

    #  Record mouse inputs until released
    global mouse_listener
    if record_mouse_movements == "yes":
        mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
    else:
        mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    mouse_listener.wait()  # wait for listener to finish starting

    #  Record keyboard inputs until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        global start_time
        start_time = time()
        listener.join()


if __name__ == '__main__':
    response = "no"
    main(response)
