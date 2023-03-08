from tkinter import *
from random import choice, shuffle
import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
           'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------- FUNCTIONS ---------------

# A function that will take the selected number of letters, numbers, and symbols, and
# select characters randomly to create a strong password


def create_password():
    unsorted_pass = []
    # Grab all the selected values for each character type
    chars = char_select.get()
    nums = num_select.get()
    syms = sym_select.get()

    # Grab the selected amount of characters from their respective arrays, stick the values into the unsorted_pass array
    for _ in range(0, chars):
        unsorted_pass.append(choice(letters))
    for _ in range(0, nums):
        unsorted_pass.append(choice(numbers))
    for _ in range(0, syms):
        unsorted_pass.append(choice(symbols))

    # scramble the order, turn the array into a string, copy the password, then display it onscreen
    shuffle(unsorted_pass)
    final_pass = "".join(unsorted_pass)
    pyperclip.copy(final_pass)
    new_pass["text"] = "Password: " + final_pass


# -------------------- UI ------------------
window = Tk()
window.config(padx=60, pady=60, bg="white")
window.title("Password Creator")

# Creates a label and scale for the amount of Letters
char_count = Label(text="Letters: ", bg="white", fg="black", pady=20)
char_count.grid(row=1, column=1)
char_select = Scale(window, from_=8, to=24, orient=HORIZONTAL, )
char_select.grid(row=1, column=2)

# Creates a label and scale for the amount of numbers
number_count = Label(text="Numbers: ", bg="white", fg="black", pady=20)
number_count.grid(row=2, column=1)
num_select = Scale(window, from_=4, to=12, orient=HORIZONTAL)
num_select.grid(row=2, column=2)

# creates a label and scale for the amount of symbols
symbol_count = Label(text="Symbols: ", bg="white", fg="black", pady=20)
symbol_count.grid(row=3, column=1)
sym_select = Scale(window, from_=2, to=6, orient=HORIZONTAL)
sym_select.grid(row=3, column=2)

# Creates a button that will run the create_password function when clicked
generate_pass = Button(text="Generate Password",
                       highlightbackground="white", command=create_password)
generate_pass.grid(row=4, column=1, columnspan=2)

# This will be edited by the create_password function to display the password
new_pass = Label(text="Password: ", bg="white", fg="black",
                 pady=15, height=2, wraplength=220)
new_pass.grid(row=5, column=0, columnspan=4)


window.mainloop()
