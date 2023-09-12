# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import PyPDF2
import Levenshtein as lev

def browse_pdf1():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf1.delete(0, tk.END)
        entry_pdf1.insert(0, file_path)

def browse_pdf2():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf2.delete(0, tk.END)
        entry_pdf2.insert(0, file_path)

def convert_pdf_to_text(file_path):
    text_set = set()
    try:
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text=""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
            words = text.split()  # Split text into words
            text_set.update(words)     # Add words to the set
        pdf_file.close()
    except Exception as e:
        return str(e)
    return text_set


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2): 
        return levenshtein_distance(s2, s1) #if length of s2 is greater than s1 then we need to swap so that
    #we can small number of iterations

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# =============================================================================

def calculate_plagiarism():
    pdf1_path = entry_pdf1.get()
    pdf2_path = entry_pdf2.get()

    if not pdf1_path or not pdf2_path:
        result_label.config(text="Please select both PDF files.")
        return

    text1_set = convert_pdf_to_text(pdf1_path)
    
    text2_set = convert_pdf_to_text(pdf2_path)
    text1 = ' '.join(text1_set)
    text2=' '.join(text2_set)
    print("text1: \n"+ text1)
    print("text2: \n"+text2)
    distance = lev.distance(text1, text2)
    max_length = max(len(text1), len(text2))
    plagiarism_percentage = (1 - (distance / max_length)) * 100

    result_label.config(text=f"Plagiarism Percentage: {plagiarism_percentage:.2f}%")

# Create the main window
window = tk.Tk()
window.title("PDF Plagiarism Checker")

# Create and arrange widgets
label1 = tk.Label(window, text="Select PDF 1:")
label1.pack()

entry_pdf1 = tk.Entry(window, width=50)
entry_pdf1.pack()

browse_button1 = tk.Button(window, text="Browse", command=browse_pdf1)
browse_button1.pack()

label2 = tk.Label(window, text="Select PDF 2:")
label2.pack()

entry_pdf2 = tk.Entry(window, width=50)
entry_pdf2.pack()

browse_button2 = tk.Button(window, text="Browse", command=browse_pdf2)
browse_button2.pack()

check_button = tk.Button(window, text="Check Plagiarism", command=calculate_plagiarism)
check_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
