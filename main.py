from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

NORMAL_FONT = ("Times of New Roman", 12)
ENTRY_TEXT_FONT = ("Times of New Roman", 10)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letter_list + symbol_list + number_list
    shuffle(password_list)

    password = "".join(password_list)
    password_text.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_text.get()
    email = email_text.get()
    password = password_text.get()

    new_data = {
        website : {
            "email" : email,
            "password" : password,
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please Don't leave any fields empty!")

    else:
        is_ok = messagebox.askyesno(title=website, message=f"There are the details entered :"
                                                   f" \nUser Name : {email} \nPaasword : {password}\n\n"
                                                   f"Is it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving Updated data
                    json.dump(data, data_file, indent=4)
            finally:
                # Clear the text boxes
                website_text.delete(0,END)
                password_text.delete(0,END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_text.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="No Data File Found.\nEnter Some data First.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email id is : {email}\n"
                                                       f"Password is : {password}")
        else:
            messagebox.showerror(title=website, message=f"No details for {website} exist.")
    finally:
        website_text.delete(0,END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200 ,height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=lock_img)
canvas.grid(column=1, row=0)

# Label
website_label = Label(text ="Website :", font=NORMAL_FONT, padx=5, pady=5)
website_label.grid(column=0, row=1)
email_label = Label(text ="Email/Username :", font=NORMAL_FONT, padx=5, pady=5)
email_label.grid(column=0, row=2)
password_label = Label(text ="Password :", font=NORMAL_FONT, padx=5, pady=5)
password_label.grid(column=0, row=3)

# Entry
website_text = Entry(width=27, font=ENTRY_TEXT_FONT)
website_text.grid(column=1, row=1)
website_text.focus()
email_text = Entry(width=45, font=ENTRY_TEXT_FONT)
email_text.grid(column=1, row=2, columnspan=2)
email_text.insert(0, "mrvaghela@gmail.com")
password_text = Entry(width=27, font=ENTRY_TEXT_FONT)
password_text.grid(column=1, row=3)

# Button
generate_password_btn = Button(text="Generate Password", width=15, command=generate_password)
generate_password_btn.grid(column=2, row=3, padx=5, pady=5)
add_btn = Button(text="Add", width=44, command=save)
add_btn.grid(column=1, row=4, columnspan=2, padx=5, pady=5)
search_btn = Button(text="Search", width=15, command=find_password)
search_btn.grid(column=2, row=1, padx=5, pady=5)

window.mainloop()
