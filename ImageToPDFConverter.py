import os
from tkinter import Tk, Button, Listbox, Label, filedialog, Scrollbar, VERTICAL, messagebox
from PIL import Image
import tkinter as tk

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.file_list = []

        self.label = Label(root, text="Selected Image Files:")
        self.label.pack()

        self.listbox = Listbox(root, selectmode="extended", width=70, height=10)
        self.listbox.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(root, orient=VERTICAL)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.add_button = Button(root, text="Add Image Files", command=self.add_files)
        self.add_button.pack()

        self.remove_button = Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack()

        self.up_button = Button(root, text="Move Up", command=lambda: self.move_selected("up"))
        self.up_button.pack()

        self.down_button = Button(root, text="Move Down", command=lambda: self.move_selected("down"))
        self.down_button.pack()

        self.convert_button = Button(root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack()

    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image files", "*.bmp;*.jpg;*.png")]
        )
        self.file_list.extend(file_paths)

        self.update_listbox()

    def remove_selected(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            del self.file_list[index]

        self.update_listbox()

    def move_selected(self, direction):
        selected_indices = self.listbox.curselection()

        if not selected_indices:
            return

        if direction == "up":
            for index in selected_indices:
                if index > 0:
                    self.file_list[index], self.file_list[index - 1] = (
                        self.file_list[index - 1],
                        self.file_list[index],
                    )
        elif direction == "down":
            for index in reversed(selected_indices):
                if index < len(self.file_list) - 1:
                    self.file_list[index], self.file_list[index + 1] = (
                        self.file_list[index + 1],
                        self.file_list[index],
                    )

        self.update_listbox()

        for index in selected_indices:
            new_index = index - 1 if direction == "up" else index + 1
            self.listbox.selection_set(new_index)

    def update_listbox(self):
        self.listbox.delete(0, "end")
        for file_path in self.file_list:
            self.listbox.insert("end", file_path)

    def convert_to_pdf(self):
        if not self.file_list:
            print("No image files selected.")
            return

        pdf_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not pdf_path.lower().endswith(".pdf"):
            pdf_path += ".pdf"

        images = [Image.open(file) for file in self.file_list]

        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:]
        )

        messagebox.showinfo("PDF Saved", f"PDF saved at: {pdf_path}")

if __name__ == "__main__":
    root = Tk()
    converter = ImageToPDFConverter(root)
    root.mainloop()