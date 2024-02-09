import tkinter as tk
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
from dotenv import load_dotenv
import os

load_dotenv(".env")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    entry_password.delete(0, 'end')
    entry_password.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title='Oops', message='Please do not leave any field empty!')
    else:
        try:
            with open('data.json', 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            # Create data file does not if it not exists
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating new data with old data
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                # Writing new data to json file
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, 'end')
            entry_password.delete(0, 'end')


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = entry_website.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title='Error', message='Data file not found.')
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {password}')
        else:
            messagebox.showwarning(title='Error', message=f'No data found for the website {website}.')


# ---------------------------- UI SETUP ------------------------------- #
root = tk.Tk()
root.title('Password Manager')
root.config(pady=70, padx=70)

logo = tk.PhotoImage(file='logo.png')
canvas = tk.Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
lbl_website = tk.Label(text='Website:  ', font=('Arial', 12, 'normal'))
lbl_website.grid(row=1, column=0)
lbl_email = tk.Label(text='Email/Username:  ', font=('Arial', 12, 'normal'))
lbl_email.grid(row=2, column=0)
lbl_password = tk.Label(text='password:  ', font=('Arial', 12, 'normal'))
lbl_password.grid(row=3, column=0)

# Entries
entry_website = tk.Entry(width=34)
entry_website.grid(row=1, column=1)
entry_website.focus()
entry_email = tk.Entry(width=52)
entry_email.grid(row=2, column=1, columnspan=2)
entry_email.insert(0, os.getenv("Email"))
entry_password = tk.Entry(width=34)
entry_password.grid(row=3, column=1)

# Buttons
btn_generate_password = tk.Button(text='Generate Password', command=generate_password)
btn_generate_password.grid(row=3, column=2)
btn_add = tk.Button(text='Add', width=44, command=save)
btn_add.grid(row=4, column=1, columnspan=2)
btn_search = tk.Button(text='Search', width=14, command=find_password)
btn_search.grid(row=1, column=2)
root.mainloop()
