import tkinter as tk
from tkinter import messagebox
import playback
import RecorderBot
import time
import os
import json

RECORDING = False

script_dir = os.path.dirname(__file__)
filepath = os.path.join(script_dir, "recordings", "actions.json")

with open(filepath, 'r') as jsonfile:
    # parse json
    data = json.load(jsonfile)


def record_movements():
    response = messagebox.askquestion(title="Record Mouse Movements?",
                                      message="Do you want to record your mouse movements?\n"
                                              "Clicks will still be recorded")
    if response == "yes":
        print("Mouse movements will be recorded")
    elif response == "no":
        print("No mouse movement will be recorded")
    return response


def countdown(seconds, callback, *args):
    global RECORDING
    # Update the countdown label
    if seconds > 1:
        countdown_label.config(text=f"Starting in {seconds} seconds...")
        root.after(1000, countdown, seconds - 1, callback, *args)
    elif seconds == 1:
        if callback == RecorderBot.main:
            countdown_label.config(text="RECORDING: PRESS ESCAPE WHEN FINISHED")
        elif callback == playback.main:
            countdown_label.config(text="RUNNING: DRAG MOUSE TO CORNER\n OF SCREEN IN EMERGENCY")
        root.after(1000, countdown, seconds - 1, callback, *args)
    elif seconds == 0:
        if callback == RecorderBot.main:
            start_recording_process(*args)
        else:
            callback(*args)  # For playback


def check_recording_status():
    global RECORDING
    if not RECORDING:
        countdown_label.config(text="Recording saved. Press PLAYBACK to begin.")
    else:
        root.after(500, check_recording_status)


def start_recording_process(response):
    global RECORDING
    RECORDING = True  # Set recording flag to True
    RecorderBot.main(response)  # Call the RecorderBot's main function
    RECORDING = False  # Reset recording flag after completion
    check_recording_status()


def start_recorder():
    response = record_movements()
    # Start the countdown
    countdown(5, RecorderBot.main, response)


def run_playback():
    global data

    max_time = max(action['time'] for action in data)  # Used to calculate rest period before next loop

    try:
        playback_count = int(playback_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for playback count.")
        return

    for num in range(playback_count):
        if num == 0:
            countdown(5, playback.main)
            time.sleep(max_time + 2)
        else:
            playback.main()
            time.sleep(max_time + 2)


root = tk.Tk()
root.title("MMO Bot")

countdown_label = tk.Label(root, text="Press RECORD to begin", font=("Helvetica", 16), fg="red")
countdown_label.pack(pady=20, padx=5)

start_recorder_button = tk.Button(root, text="RECORD", command=start_recorder)
start_recorder_button.pack(pady=20, padx=5)


run_playback_button = tk.Button(root, text="PLAYBACK", command=run_playback)
run_playback_button.pack(pady=20, padx=5)

playback_label = tk.Label(root, text="Playback how many times?")
playback_label.pack(pady=5, padx=5)

playback_entry = tk.Entry(root)
playback_entry.pack(pady=10, padx=5)

root.mainloop()
