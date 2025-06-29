from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import os
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------------- SETTING MASTER PASSWORD ---------------------------#


def set_master_password():
    entered_password = master_password_entry.get()
    hashed_password = hash_password(entered_password)
    with open("master_password.txt", "w") as file:
        file.write(hashed_password)
    messagebox.showinfo(title="Success", message="Master password set successfully!")
    auth_window.destroy()
    main_window()

# -------------------------------- CHECK MASTER PASSWORD ---------------------------#


def check_master_password():
    entered_password = master_password_entry.get()
    hashed_password = hash_password(entered_password)
    try:
        with open("master_password.txt", "r") as file:
            saved_password = file.read()

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No master password found! Set it first.")

    else:
        if hashed_password == saved_password:
            auth_window.destroy()
            main_window()
        else:
            messagebox.showerror(title="Error", message="Incorrect Master Password!")

# -------------------------------- PASSWORD GENERATOR ---------------------------#
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ------------------------------ SAVE PASSWORD ---------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="ERROR", message="Please make sure you haven't left any fields empty.")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    #reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                #updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    #saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                    website_entry.delete(0, END)
                    email_entry.delete(0, END)
                    password_entry.delete(0, END)

# -------------------------------- FIND PASSWORD ----------------------------------#
def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left website field empty")
    else:
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="ERROR", message="No Data File Found.")
        else:
            if website in data:
                email = data[website]["Email"]
                password = data[website]["Password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="ERROR", message=f"no details exist for {website}.")
        finally:
            website_entry.delete(0, END)


# -------------------------------- UI SETUP ----------------------------------#
def main_window():
    global password_entry, website_entry, email_entry
    window = Tk()
    window.title("Password Manager")
    window.config(padx=50, pady=50)

    # Image
    canvas = Canvas(width=200, height=200)
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(row=0, column=1)

    # Labels
    website_label = Label(text="Website:")
    website_label.grid(row=1, column=0)

    email_label = Label(text="Email/Username:")
    email_label.grid(row=2, column=0)

    password_label = Label(text="Password:")
    password_label.grid(row=3, column=0)

    # Entries
    website_entry = Entry(width=35)
    website_entry.grid(row=1, column=1)


    email_entry = Entry(width=53)
    email_entry.grid(row=2, column=1, columnspan=2)

    password_entry = Entry(width=35)
    password_entry.grid(row=3, column=1)

    # Buttons
    generate_password_button = Button(text="Generate Password", command=generate_password)
    generate_password_button.grid(row=3, column=2)

    add_button = Button(text="Add", width=36, command=save)
    add_button.grid(row=4, column=1, columnspan=2)

    search_button = Button(text="Search", width=13, command=find_password)
    search_button.grid(row=1, column=2)

    window.mainloop()


# -------------------------------- AUTHENTICATION UI SETUP ----------------------------------#
auth_window = Tk()
auth_window.title("Authentication")
auth_window.config(padx=50, pady=50)

enter_master_password_label = Label(text="Enter Master Password:")
enter_master_password_label.grid(row=0, column=0)

master_password_entry = Entry(width=35, show="*")
master_password_entry.grid(row=1, column=0)
master_password_entry.focus()

# Buttons for setting/checking password
if os.path.exists("master_password.txt"):
    login_button = Button(text="Login", width=15, command=check_master_password)
    login_button.grid(row=2, column=0)
else:
    set_master_password_button = Button(text="Set Master Password", width=15, command=set_master_password)
    set_master_password_button.grid(row=2, column=0)

auth_window.mainloop()
