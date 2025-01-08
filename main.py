from tkinter import *
from tkinter import Tk, Label, Button, Text, RIGHT, Y, LEFT, BOTH
from PIL import Image, ImageTk
from utils.scan import Scan
from utils.definitions import update_definitions
import os


def main():
    # Build Shitty ass UI
    root = Tk()
    root.title("Shadow Anti-Virus")
    root.geometry("600x400")  # Increased width to accommodate the text box

    root_frame = Frame(root)
    root_frame.pack(fill=BOTH, expand=True)

    # Configure grid layout
    root_frame.grid_columnconfigure(0, minsize=250)  # Set minimum width for left panel
    root_frame.grid_columnconfigure(1, weight=1)  # Allow right panel to expand
    root_frame.grid_rowconfigure(0, weight=1)

    left_panel = Frame(root_frame)
    left_panel.grid(row=0, column=0, sticky="nsew")

    right_panel = Frame(root_frame)
    right_panel.grid(row=0, column=1, sticky="nsew")

    # Title that says welcome to Shadow AV
    welcome_label = Label(left_panel, text="Welcome to Shadow AV")
    welcome_label.pack(pady=20)

    # Image of the Shadow AV logo
    logo_image = Image.open("images/shadow.gif")

    # Resize the image to fit within the desired dimensions (e.g., 300x300)
    max_width, max_height = 200, 200
    logo_image.thumbnail((max_width, max_height))

    logo = ImageTk.PhotoImage(logo_image, master=root)
    logo_label = Label(left_panel, image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=20)


    # Create a text box
    text_box = Text(right_panel, wrap='word', font=("Helvetica", 12), bg="black", fg="white")
    text_box.insert('1.0', "> 2025 Shadow AV © Big Balls Bird Inc")
    text_box.config(state=DISABLED)
    text_box.pack(side=LEFT, fill=BOTH, expand=True)

    # check if there is a definitions file in the definitions folder
    # if not then download the latest definitions file
    if not os.path.exists("definitions/full.csv"):
        text_box.config(state=NORMAL)
        text_box.insert(END, "\n> Downloading latest definitions file...")
        text_box.config(state=DISABLED)
        update_definitions()
        text_box.config(state=NORMAL)
        text_box.insert(END, "\n> Definitions file updated successfully!")
        text_box.config(state=DISABLED)


    # initialize scanner and give it access to the textbox for output
    virus_scanner = Scan(text_box)
    # Button that says scan with design elements and hover effects
    scan_button = Button(left_panel, text="Run Full Scan", bg="lightgray", fg="black", font=("Helvetica", 12, "bold"), relief="raised", bd=3, command= lambda: virus_scanner.run_scan())
    scan_button.pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    main()