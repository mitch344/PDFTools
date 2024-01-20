import os
from tkinter import Tk, Button, Listbox, Label, filedialog, Scrollbar, VERTICAL, messagebox
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk

class PDFMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.file_list = []

        self.label = Label(root, text="Selected PDF Files:")
        self.label.pack()

        self.listbox = Listbox(root, selectmode="extended", width=70, height=10)
        self.listbox.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(root, orient=VERTICAL)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.add_button = Button(root, text="Add PDF Files", command=self.add_files)
        self.add_button.pack()

        self.remove_button = Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack()

        self.up_button = Button(root, text="Move Up", command=lambda: self.move_selected("up"))
        self.up_button.pack()

        self.down_button = Button(root, text="Move Down", command=lambda: self.move_selected("down"))
        self.down_button.pack()

        self.merge_button = Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack()

    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf")]
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

    def merge_pdfs(self):
        if not self.file_list:
            print("No PDF files selected.")
            return

        output_pdf_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not output_pdf_path.lower().endswith(".pdf"):
            output_pdf_path += ".pdf"

        pdf_writer = PdfWriter()

        for pdf_file in self.file_list:
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        messagebox.showinfo("PDFs Merged", f"PDFs merged and saved at: {output_pdf_path}")

if __name__ == "__main__":
    root = Tk()
    merger = PDFMerger(root)
    root.mainloop()