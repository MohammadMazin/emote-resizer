import io
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
from imageResizer import ImageResizer

root = tk.Tk()
app = ImageResizer(root)
root.mainloop()
