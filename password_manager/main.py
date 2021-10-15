import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_clicked():
    website_input = str(website_entry.get()).title()
    user_input = str(user_entry.get())
    password_input = str(password_entry.get())
    new_data = {
        website_input: {
            "Email": user_input,
            "Password": password_input,
        }
    }

    if len(website_input) == 0:
        messagebox.showerror(title="Oops", message="Website cannot be blank!")

    elif len(user_input) == 0:
        messagebox.showerror(title="Oops", message="Email/Username cannot be blank!")

    elif len(password_input) == 0:
        messagebox.showerror(title="Oops", message="Password cannot be blank!")

    else:
        is_yes = messagebox.askyesno(title=website_input, message=f"These are the details you entered:\n"
                                                                  f"Email: {user_input}\nPassword: {password_input}\n"
                                                                  f"Is it ok to save?")

        if is_yes:
            pyperclip.copy(password_input)
            try:
                with open("data.json", "r") as data_file:
                    # Reading old Data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old Data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, "end")
                password_entry.delete(0, "end")


def find_password():
    website_input = str(website_entry.get()).title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")

    else:
        if website_input in data:
            email = data[website_input]["Email"]
            password = data[website_input]["Password"]
            messagebox.showinfo(title=website_input, message=f"Email: {email}\nPassword: {password}")

        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_input} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
# window.minsize(width=800, height=600)
window.title("Password Manager by AntonyCJA")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry(width=25)
website_entry.grid(column=1, row=1, columnspan=1)
website_label.config(padx=10, pady=5)
website_entry.focus()

user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)
user_entry = Entry(width=44)
user_entry.grid(column=1, row=2, columnspan=2)
user_label.config(padx=10, pady=5)
user_entry.insert(0, "cja@gmail.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=25)
password_entry.grid(column=1, row=3, columnspan=1)
password_label.config(padx=10, pady=5)

generate_pas = Button(text="Generate Password", command=generate_password)
generate_pas.grid(column=2, row=3)
generate_pas.config(padx=10, pady=5)

search_btn = Button(text="Search", width=15, command=find_password)
search_btn.grid(column=2, row=1, columnspan=1)
search_btn.config(padx=12, pady=5)

add = Button(text="Add", width=41, command=add_clicked)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
