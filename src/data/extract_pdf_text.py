"""
Module: extract_pdf_text.py
Purpose: Extract raw text from official PDF documents page by page using PyMuPDF (fitz),
saving the raw extraction output into dataset/interim/pdf_pages.csv.
"""

import os
import json
import pandas as pd
import pymupdf  # PyMuPDF

def extract_all_pages(config_path="config/sources.json", output_csv="dataset/interim/pdf_pages.csv"):
    with open(config_path, "r") as f:
        config = json.load(f)
        
    extracted_rows = []
    print("Starting PDF text extraction across all documents...")
    
    total_pages = 0
    for src in config["sources"]:
        pdf_path = src["local_path"]
        if not os.path.exists(pdf_path):
            print(f"Warning: File {pdf_path} not found. Skipping.")
            continue
            
        doc = pymupdf.open(pdf_path)
        num_pages = len(doc)
        total_pages += num_pages
        
        for page_idx in range(num_pages):
            page = doc[page_idx]
            page_text = page.get_text("text")
            extracted_rows.append({
                "academic_year": src["academic_year"],
                "year_num": src["year_num"],
                "cap_round": src["cap_round"],
                "document_type": src["document_type"],
                "pdf_name": src["file_name"],
                "source_url": src["url"],
                "page_no": page_idx + 1,
                "page_text": page_text
            })
        doc.close()
        print(f"Extracted {num_pages} pages from {src['file_name']}")
        
    df_pages = pd.DataFrame(extracted_rows)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_pages.to_csv(output_csv, index=False)
    print(f"Successfully extracted {total_pages} total pages across all documents into {output_csv}")
    return df_pages

if __name__ == "__main__":
    extract_all_pages()

