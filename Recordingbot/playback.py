import pyautogui
import pydirectinput
import time
import os
import json


def main():

    initializePyAutoGUI()

    # Countdown timer
    # countdownTimer()

    playActions("actions.json")

    # done
    print("Done")


def initializePyAutoGUI():
    pyautogui.FAILSAFE = True  # in emergency move mouse to upper left of screen


def countdownTimer():

    print("Starting", end="")
    for i in range(0, 5):
        print(".", end="")
        time.sleep(1)
    print("Go")


def playActions(filename):

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir,
        'recordings',
        filename)

    with open(filepath, 'r') as jsonfile:
        # parse json
        data = json.load(jsonfile)
        #  print(data)

    data = [{**action, 'button': convertKey(action['button'])} for action in data]

    # loop over each action
    for index, action in enumerate(data):  # we want two actions so we need index and action
        start_time = time.time()
        action_start_time = time.time()

        # look for escape input to exit
        if action['button'] == 'Key.esc':
            break

        if action['type'] == 'move':
            pydirectinput.move(action['pos'][0], action['pos'][1])
        elif action['type'] == 'keyDown':
            key = action['button']
            pydirectinput.keyDown(key)
        elif action['type'] == "keyUp":
            key = action['button']
            pydirectinput.keyUp(key)
        elif action['type'] == "click":
            key = action['button']
            pydirectinput.click(action['pos'][0], action['pos'][1], button=key)

        # sleep between actions
        try:
            next_action = data[index + 1]
        except IndexError:
            break
        elapsed_time = next_action['time'] - action['time']

        if elapsed_time < 0.00:
            raise Exception('Unexpected action ordering time less than 0')

        action_end_time = time.time()
        elapsed_time -= (action_end_time - action_start_time)
        if elapsed_time < 0.00:  # accounts for very quick key presses
            elapsed_time = 0.00
        print(f'sleeping for {elapsed_time}')
        time.sleep(elapsed_time)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The loop took {elapsed_time:.4f} seconds to run.")


def convertKey(button):
    # compare differences in keys pynput and pyautogui then convert to pyautogui

    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
        'middle pos': 'middle',
        'Button.left': 'left',
        'Button.right': 'right',
    }

    cleaned_key = button.replace('Key.', '').replace('Button.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key


if __name__ == "__main__":
    main()
