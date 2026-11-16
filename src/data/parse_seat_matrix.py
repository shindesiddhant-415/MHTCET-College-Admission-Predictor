"""
Module: parse_seat_matrix.py
Purpose: Convert extracted text from Seat Matrix PDFs into a normalized CSV.
Schema:
academic_year, institute_code, institute_name, course_code, branch_name,
institute_status, total_intake, state_seats, minority_seats, all_india_seats,
institute_seats, orphan_seats, source_file, source_page
"""

import os
import re
import pandas as pd

def parse_seat_matrix_page(row):
    academic_year = row["academic_year"]
    source_file = row["pdf_name"]
    source_page = int(row["page_no"])
    page_text = str(row["page_text"])
    
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    parsed_rows = []
    
    current_inst_code = None
    current_inst_name = None
    current_status = None
    
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        
        # Check for Institute Header: e.g. "06006 - COEP Technological University, Pune (Government Autonomous)"
        inst_match = re.match(r'^(\d{5})\s*-\s*([^(]+)(?:\(([^)]+)\))?$', line)
        if inst_match and not ("Course Code" in line or "Branch Name" in line):
            current_inst_code = inst_match.group(1).strip()
            current_inst_name = inst_match.group(2).strip()
            if inst_match.group(3):
                current_status = inst_match.group(3).strip()
            i += 1
            continue
            
        # Check for Course Code row (10 digits)
        if re.match(r'^\d{10}$', line):
            course_code = line
            i += 1
            if i < n:
                branch_name = lines[i]
                i += 1
                
                # Next 6 numbers: Intake, State Seats, Minority, AI Seats, Inst Seats, Orphan
                numeric_vals = []
                while i < n and len(numeric_vals) < 6:
                    if re.match(r'^\d+$', lines[i]):
                        numeric_vals.append(int(lines[i]))
                        i += 1
                    else:
                        break
                        
                if len(numeric_vals) == 6:
                    parsed_rows.append({
                        "academic_year": academic_year,
                        "institute_code": current_inst_code if current_inst_code else course_code[:5],
                        "institute_name": current_inst_name,
                        "course_code": course_code,
                        "branch_name": branch_name,
                        "institute_status": current_status,
                        "total_intake": numeric_vals[0],
                        "state_seats": numeric_vals[1],
                        "minority_seats": numeric_vals[2],
                        "all_india_seats": numeric_vals[3],
                        "institute_seats": numeric_vals[4],
                        "orphan_seats": numeric_vals[5],
                        "source_file": source_file,
                        "source_page": source_page
                    })
            continue
            
        i += 1
        
    return parsed_rows

def parse_all_seat_matrices(interim_csv="dataset/interim/pdf_pages.csv", output_csv="dataset/processed/seat_matrix.csv"):
    df_pages = pd.read_csv(interim_csv)
    df_sm = df_pages[df_pages["document_type"] == "seat_matrix"]
    
    all_parsed = []
    print(f"Parsing seat matrix tables from {len(df_sm)} pages...")
    for _, row in df_sm.iterrows():
        records = parse_seat_matrix_page(row)
        all_parsed.extend(records)
        
    df_res = pd.DataFrame(all_parsed)
    # Ensure institute names are filled
    inst_map = df_res.dropna(subset=['institute_name']).drop_duplicates(subset=['institute_code']).set_index('institute_code')['institute_name'].to_dict()
    df_res['institute_name'] = df_res['institute_name'].fillna(df_res['institute_code'].map(inst_map))
    
    print(f"Total parsed seat matrix rows: {len(df_res)}")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_res.to_csv(output_csv, index=False)
    print(f"Saved normalized seat matrix to {output_csv}")
    print(df_res.head(5))
    return df_res

if __name__ == "__main__":
    parse_all_seat_matrices()
