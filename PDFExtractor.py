import os
from tkinter import Tk, Button, Label, filedialog, Entry, StringVar, messagebox
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk

class PDFPageExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Page Extractor")

        self.input_pdf_path = StringVar()
        self.start_page_var = StringVar()
        self.end_page_var = StringVar()

        self.label = Label(root, text="Select PDF File:")
        self.label.pack()

        self.select_button = Button(root, text="Select PDF", command=self.select_pdf)
        self.select_button.pack()

        self.start_label = Label(root, text="Start Page:")
        self.start_label.pack()

        self.start_entry = Entry(root, textvariable=self.start_page_var)
        self.start_entry.pack()

        self.end_label = Label(root, text="End Page:")
        self.end_label.pack()

        self.end_entry = Entry(root, textvariable=self.end_page_var)
        self.end_entry.pack()

        self.extract_button = Button(root, text="Extract Pages", command=self.extract_pages)
        self.extract_button.pack()

    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf")]
        )
        self.input_pdf_path.set(pdf_path)

    def extract_pages(self):
        pdf_path = self.input_pdf_path.get()
        start_page = self.start_page_var.get()
        end_page = self.end_page_var.get()

        if not (pdf_path and start_page and end_page):
            messagebox.showwarning("Missing Information", "Please provide all required information.")
            return

        try:
            start_page = int(start_page)
            end_page = int(end_page)
        except ValueError:
            messagebox.showerror("Invalid Input", "Start Page and End Page must be valid integers.")
            return

        if start_page > end_page:
            messagebox.showerror("Invalid Range", "Start Page should be less than or equal to End Page.")
            return

        output_pdf_path = filedialog.asksaveasfilename(
            title="Save Extracted Pages As",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not output_pdf_path.lower().endswith(".pdf"):
            output_pdf_path += ".pdf"

        pdf_writer = PdfWriter()

        with open(pdf_path, "rb") as input_pdf:
            pdf_reader = PdfReader(input_pdf)
            for page_num in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        messagebox.showinfo("Pages Extracted", f"Pages {start_page} to {end_page} extracted and saved at: {output_pdf_path}")

if __name__ == "__main__":
    root = Tk()
    extractor = PDFPageExtractor(root)
    root.mainloop()
