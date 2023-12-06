# Script to record keys for research purposes
from pynput import mouse, keyboard
import pyautogui
import datetime
import time
import tkinter as tk
from threading import Thread

# SET DEFAULT VALUE FOR RECORDING
recording = True
# Global variable for the listeners
key_listener = None
mouse_listener = None

# SETTINGS FOR KEYLOGGER
def on_press(key):
    # Start listening
    with open("RECORDER - Keys.txt", "a") as f:
        f.write(str(key) + '    ' + str(datetime.datetime.now()) + '\n')

def on_release(key):
    # Stop listening
    if not recording:
        return False
    
# SETTINGS FOR MOUSE TRACKER
def on_move(x, y):
    with open("RECORDER - Mouse.txt", "a") as f:
        f.write("Mouse: Move%s Time: %s \n" %((x, y),datetime.datetime.now()))

def on_click(x, y, button, pressed):
    with open("RECORDER - Mouse.txt", "a") as f:
        if pressed:
            f.write("Mouse: Click%s Time: %s \n" %((x, y,button,pressed),datetime.datetime.now()))
        else:
            f.write("Mouse: Released%s Time: %s \n" %((x,y,button,pressed),datetime.datetime.now()))

# SETTINGS FOR SCREEN CAPTURE
def take_screnshot():
    myscreenshot = pyautogui.screenshot()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    myscreenshot.save(f'RECORDER - {timestamp}.png')

# RECORDER
def start_recording():
    global key_listener
    if recording:
        #ADD KEYS
        key_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        key_listener.start()

        #ADD MOUSE
        mouse_listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click)
        mouse_listener.start()

        #ADD CURSOR AND SCREENSHOTS
        logging_start_time = time.time()
        while recording == True:
            print("Cursor: %s Time: %s" %(pyautogui.position(), datetime.datetime.now()),file=open("RECORDER - Cursor.txt",'a+'))
            #Make the function wait for 0.25 seconds to reduce output
            time.sleep(0.25)
            #Take a screenshot every 60 seconds
            elapsed_seconds = time.time() - logging_start_time
            if elapsed_seconds > 60:
                take_screnshot()
                logging_start_time = time.time() #Reset the timer
                #print("screenshot loop", datetime.datetime.now())           

        #ADD SCREEN RESOLUTION
        print(pyautogui.size(),file=open("RECORDER - Resolution.txt","w+"))

# GUI Functions
def start_recording_gui():
    global recording
    recording = True
    Thread(target=start_recording).start()  # Start recording in a separate thread

def stop_recording_gui():
    global recording
    recording = False

def on_close(): #when the window is closed, stop running
    global key_listener
    global mouse_listener
    stop_recording_gui()
    if key_listener is not None:
        key_listener.stop()
    if mouse_listener is not None:
        mouse_listener.stop()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Research keylogger")


start_button = tk.Button(root, text="Start Recording", command=start_recording_gui)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording_gui)
stop_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
