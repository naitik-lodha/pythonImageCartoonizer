import customtkinter as ctk
from tkinter import filedialog, Image
import imageCartoonizer
from PIL import Image

global file_path


def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    return file_path


def cartoonize(file_path):

    output = imageCartoonizer.cartoonize_image(file_path)
    image = ctk.CTkImage(Image.open(output), size=(300, 300))
    imageLabel.configure(text="", image=image)
    cartoonizeButton.configure(state="disabled")


def process_file(file_path):
    if file_path is not None:
        # Process the selected file
        print("Selected file:", file_path)
        image = ctk.CTkImage(Image.open(file_path), size=(300, 300))
        imageLabel.configure(image=image)
        cartoonizeButton.configure(state="normal")
        progressBar.set(0)

        print("Done")
    else:
        imageLabel.configure(text="No file found")


root = ctk.CTk()
root.title("Toonify")
root.geometry("760x580")


headingLabel=ctk.CTkLabel(root,text=
                          "Toonify",font=("Comic Sans MS",65))
headingLabel.pack(pady=10)
select_file_button = ctk.CTkButton(root, text="Select File", command=lambda: process_file(select_file()))
select_file_button.pack(pady=10)

imageLabel = ctk.CTkLabel(root, text="")
imageLabel.pack(pady=10)

cartoonizeButton = ctk.CTkButton(root, text="Cartoonize Image", command=lambda: cartoonize(file_path), state="disabled")
cartoonizeButton.pack(pady=5)

progressBar=ctk.CTkProgressBar(root,width=300,mode="indeterminate")
progressBar.set(0)
progressBar.pack()


root.mainloop()
