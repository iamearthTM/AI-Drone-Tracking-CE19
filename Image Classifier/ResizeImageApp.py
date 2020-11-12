#!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pathlib
import os
import re
from keras.preprocessing.image import load_img
from PIL import Image
import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk

class Gui_folder():
    def __init__(self, path="/"):
        self.height = 500
        self.width = 800 
        self.root = tk.Tk()
        self.root.title("Resize Image")
        self.root.resizable(False, False) 

        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()
        self.image_width = tk.IntVar(value=256)
        self.image_width.trace("w", self.__validate_inputs_state)
        self.image_height = tk.IntVar(value=256)
        self.image_height.trace("w", self.__validate_inputs_state)
        self.is_saving = False

        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width)
        self.canvas.pack()

        self.input_frame = tk.Frame(self.root, bg='#80c1ff', bd=5)
        self.input_frame.place(relx=0.5, rely=0, relwidth=0.75, relheight=0.1, anchor='n')
        self.top_frame = tk.Frame(self.root, bg='#80c1ff', bd=5)
        self.top_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
        self.middle_frame = tk.Frame(self.root, bg='#80c1ff', bd=5)
        self.middle_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.1, anchor='n')
        self.bottom_frame = tk.Frame(self.root, bd=5)
        self.bottom_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.1, anchor='n')

        self.label_width = tk.Label(self.input_frame, text="Width:")
        self.label_width.place(relx=0, relwidth=0.1, relheight=1)
        self.input_width = tk.Entry(self.input_frame, font=40, textvariable=self.image_width)
        self.input_width.place(relx=0.1, relwidth=0.35, relheight=1)

        self.label_height = tk.Label(self.input_frame, text="Height:")
        self.label_height.place(relx=0.55, relwidth=0.1, relheight=1)
        self.input_height = tk.Entry(self.input_frame, font=40, textvariable=self.image_height)
        self.input_height.place(relx=0.65, relwidth=0.35, relheight=1)

        self.label_source = tk.Label(self.top_frame, textvariable=self.source_path)
        self.label_source.place(relwidth=0.65, relheight=1)
        self.button_source = tk.Button(self.top_frame, text="Browse", command=self.__browse_source, font=40)
        self.button_source.place(relx=0.7, relwidth=0.3, relheight=1)

        self.label_target = tk.Label(self.middle_frame, textvariable=self.target_path)
        self.label_target.place(relwidth=0.65, relheight=1)
        self.button_target = tk.Button(self.middle_frame, text="Save Folder", command=self.__browse_target, font=40)
        self.button_target.place(relx=0.7, relwidth=0.3, relheight=1)

        self.button_start = tk.Button(self.bottom_frame, text="Start", command=self.__save_images, font=40, state=tk.DISABLED)
        self.button_start.place(relx=0.4, relwidth=0.3, relheight=1)

        self.root.mainloop()


    def __browse_source(self):
        filename = tk.filedialog.askdirectory()
        self.source_path.set(filename + "/")
        self.__validate_inputs_state()


    def __browse_target(self):
        filename = tk.filedialog.askdirectory()
        self.target_path.set(filename + "/")
        self.__validate_inputs_state()


    def __validate_inputs_state(self):
        is_image_inputs_zero = not self.image_height.get() and not self.image_width.get()
        is_disable_start = not self.target_path.get() or not self.source_path.get() or self.is_saving or is_image_inputs_zero

        self.button_start.configure(state=tk.DISABLED) if is_disable_start else self.button_start.configure(state=tk.NORMAL)
        self.button_target.configure(state=tk.DISABLED) if self.is_saving else self.button_target.configure(state=tk.NORMAL)
        self.button_source.configure(state=tk.DISABLED) if self.is_saving else self.button_source.configure(state=tk.NORMAL)

    def __atoi(self, text):
        return int(text) if text.isdigit() else text


    def __natural_keys(self, text):
        return [self.__atoi(c) for c in re.split(r'(\d+)', str(text))]


    def __convert_dir_to_list(self):
        data_dir = pathlib.Path(str(self.source_path.get()))
        files_list = list(data_dir.glob("**/*"))
        files_list = sorted(files_list, key=self.__natural_keys)

        return files_list

    def __save_images(self):
        print("start save image(s)")
        isYes = tk.messagebox.askokcancel(title="Save Image", message="Do you want to start ?")

        if not isYes:
            return False

        try:
            width = int(self.image_height.get())
            height = int(self.image_height.get())
        except ValueError:
            tk.messagebox.showerror(title="Save Image", message="Width and Height must be integer")
            return False

        self.is_saving = True
        self.__validate_inputs_state()

        images = self.__convert_dir_to_list()

        for index, path in enumerate(images):
            save_path = str(self.target_path.get()) + str(index + 1) + ".jpg"
            image = load_img(path)
            image = image.resize((width, height))
            image_array = np.asarray(image)

            if os.path.exists(save_path):
                tk.messagebox.showerror(title="Save Image", message=save_path + " is exist")
                print(save_path, "is exist")
                self.is_saving = False
                self.__validate_inputs_state()

                return False

            img = Image.fromarray(image_array)
            img.save(save_path)

        self.is_saving = False
        self.__validate_inputs_state()
        print("success save image(s)")
        tk.messagebox.showinfo(title="Save Image", message="Completed")


Gui_folder()


