import io
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, UnidentifiedImageError
from menuBar import MenuBar


class ImageResizer:
    def __init__(self, master):
        self.master = master
        master.title("Image Resizer")
        master.minsize(1000, 400)
        master.maxsize(1000, 1400)

        MenuBar(master)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure('TButton', foreground='#ffffff', background='#383838', font=(
            'Helvetica', 14), padding=10, width=20, anchor='center')
        style.map('TButton', foreground=[('active', '#383838'), ('disabled', '#919191')], background=[
                  ('active', '#ffffff'), ('disabled', '#d9d9d9')])

        # Create buttons
        self.select_button = ttk.Button(
            master, text="Select Images", command=self.load_images)
        self.resize_72_button = ttk.Button(
            master, text="Resize for Sub Badges", command=lambda: self.resize_images("badges"), state="disabled")
        self.resize_128_button = ttk.Button(
            master, text="Resize for bits", command=lambda: self.resize_images("bits"), state="disabled")
        self.clear_button = ttk.Button(
            master, text="Clear Images", command=self.clear_images)
        # self.save_button = tk.Button(
        #     master, text="Save Resized Images", command=self.save_images, state="disabled")

        # Create image preview
        self.preview = tk.Label(master)

        self.select_button.grid(row=0, column=0, padx=10, pady=10)
        self.resize_72_button.grid(row=1, column=0, padx=10, pady=10)
        self.resize_128_button.grid(row=2, column=0, padx=10, pady=10)
        # self.save_button.grid(row=3, column=0, padx=10, pady=10)
        self.clear_button.grid(row=3, column=0, padx=10, pady=10)

        # Create image preview
        self.canvas = tk.Canvas(master, bg='white', bd=1,
                                relief="solid", highlightthickness=0)
        self.canvas.grid(row=0, column=1, rowspan=4,
                         padx=10, pady=10, sticky=tk.NSEW)
        self.scrollbar = tk.Scrollbar(
            master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=2, rowspan=4, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Set column and row weights
        master.columnconfigure(0, weight=1, minsize=150)
        master.columnconfigure(1, weight=3)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)

        # Initialize variables
        self.images = []
        self.resized_images = []

        if len(self.images) == 0:
            self.preview.config(text="Click to select images")

    def clear_images(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.images = []

    def on_enter(self, event):
        self.preview.config(cursor="hand2", bg="#f5f5f5")

    def on_leave(self, event):
        self.frame.config(cursor="", bg="white")

    def load_images(self):
        # Open file dialog to select both JPG and PNG when dialog opens

        filetypes = (("JPEG files", "*.jpg, *.png"), ("PNG files", "*.png"))

        images = filedialog.askopenfilenames(
            title="Select image files", filetypes=filetypes)

        # Load images and display preview
        valid_images = []
        for image in images:
            if os.path.isfile(image):
                try:
                    img = Image.open(image)
                    valid_images.append(image)
                except (UnidentifiedImageError, IOError):
                    messagebox.showerror(
                        "Error", IOError, icon="warning")
                    pass

        self.images.extend(valid_images)

        if len(self.images) > 0:
            self.resize_72_button.config(state="normal")
            self.resize_128_button.config(state="normal")
            # self.save_button.config(state="normal")

            # Show images in preview
            num_columns = 4  # set the number of columns
            for i, image in enumerate(self.images):
                if os.path.isfile(image):
                    img = Image.open(image)
                    img.thumbnail((128, 128))
                    photo = ImageTk.PhotoImage(img)
                    label = tk.Label(self.frame, image=photo, bg="white")
                    label.image = photo
                    label.grid(row=i // num_columns, column=i %
                               num_columns, padx=10, pady=10, sticky="w")

    def resize_images(self, size):
        save_path = filedialog.askdirectory(
            title="Save Resized Images")

        sizes = []
        if size == "badges":
            sizes = [(128, 128), (72, 72), (36, 36), (18, 18)]
        elif size == "bits":
            sizes = [(72, 72), (32, 32), (18, 18)]

        # Resize each image in the list
        try:
            for image_path in self.images:
                for s in sizes:
                    with open(image_path, 'rb') as f:
                        img = Image.open(io.BytesIO(f.read()))
                        img = img.resize(s, resample=Image.LANCZOS)

                    # Save the resized image
                    file_name, ext = os.path.splitext(
                        os.path.basename(image_path))
                    resized_file_name = os.path.join(
                        save_path, file_name + "_" + str(s) + ext)
                    img.save(resized_file_name)
            messagebox.showinfo("Success", "Images resized successfully")
        except (UnidentifiedImageError, IOError):
            messagebox.showerror(
                "Error", IOError, icon="warning")

    def save_images(self):
        # Save resized images
        if not self.resized_images:
            return

        filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"))
        filename = filedialog.asksaveasfilename(
            filetypes=filetypes, defaultextension=".png")

        if filename:
            for i, image in enumerate(self.resized_images):
                image.save(f"{filename}_{i}.png")

    def show_preview(self, image):
        # Display image in preview
        img = ImageTk.PhotoImage(image)
        self.preview.configure(image=img)
        self.preview.image = img
