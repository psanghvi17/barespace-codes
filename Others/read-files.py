import os
import pdfplumber

# Folder to scan for PDF files
FOLDER_PATH = './spaces'

def check_percentage_on_third_page(folder_path):
    # Walk through all files and subfolders in the given folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a PDF
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    # Open the PDF file
                    with pdfplumber.open(file_path) as pdf:
                        # Check if the PDF has at least 3 pages
                        if len(pdf.pages) >= 3:
                            # Extract text from the 3rd page (index 2)
                            third_page_text = pdf.pages[2].extract_text()
                            if third_page_text and '%' in third_page_text:
                                continue
                                #print(f"The file '{file}' contains '%' on the 3rd page.")
                            else:
                                print(f"The file '{file}' does not contain '%' on the 3rd page.")
                        else:
                            print(f"The file '{file}' has less than 3 pages.")
                except Exception as e:
                    print(f"Could not process file '{file}': {e}")

# Usage
check_percentage_on_third_page(FOLDER_PATH)
