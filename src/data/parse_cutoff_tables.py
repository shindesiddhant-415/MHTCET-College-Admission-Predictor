"""
Module: parse_cutoff_tables.py
Purpose: Convert extracted text from CAP cutoff PDFs into a clean, normalized, long-format CSV.
Target schema:
academic_year, year_num, cap_round, seat_type, institute_code, institute_name,
institute_status, course_code, branch_name, seat_pool, seat_category_code,
stage_code, merit_no, cutoff_percentile, source_file, source_page
"""

import os
import re
import pandas as pd

KNOWN_CATEGORIES = [
    "GOPENS", "LOPENS", "GOBCS", "LOBCS", "EWS", "TFWS",
    "GSCS", "LSCS", "GSTS", "LSTS", "GVJS", "LVJS",
    "GNT1S", "GNT2S", "GNT3S", "DEFOPENS", "PWDOPENS", "ORPHAN"
]

def parse_cutoff_page_text(row):
    academic_year = row["academic_year"]
    year_num = int(row["year_num"])
    cap_round = int(row["cap_round"])
    source_file = row["pdf_name"]
    source_page = int(row["page_no"])
    page_text = str(row["page_text"])
    
    # Normalize newline inside parentheses e.g. (98.9418\n28) -> (98.941828)
    cleaned = re.sub(r'\(\s*([0-9.]+)\s*\n\s*([0-9]+)\s*\)', r'(\1\2)', page_text)
    cleaned = re.sub(r'\(\s*([0-9.]+)\s*\)', r'(\1)', cleaned)
    
    lines = [l.strip() for l in cleaned.split('\n') if l.strip()]
    
    parsed_rows = []
    
    current_inst_code = None
    current_inst_name = None
    current_course_code = None
    current_branch_name = None
    current_status = None
    current_pool = None
    
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        
        # Check for Institute Header: e.g. "06006 - COEP Technological University, Pune"
        if re.match(r'^\d{5}\s*-', line) and not ("|" in line or "Status:" in line):
            parts = line.split('-', 1)
            current_inst_code = parts[0].strip()
            current_inst_name = parts[1].strip()
            i += 1
            continue
            
        # Check for Course Header: e.g. "0600624510 - Computer Engineering | Status: ... | Seat Pool: ..."
        if re.match(r'^\d{10}\s*-', line):
            pipe_parts = [p.strip() for p in line.split('|')]
            c_part = pipe_parts[0]
            if '-' in c_part:
                c_code, b_name = c_part.split('-', 1)
                current_course_code = c_code.strip()
                current_branch_name = b_name.strip()
            for p in pipe_parts[1:]:
                if "Status:" in p:
                    current_status = p.replace("Status:", "").strip()
                elif "Seat Pool:" in p:
                    current_pool = p.replace("Seat Pool:", "").strip()
            i += 1
            continue
            
        # Check for Table Header "Stage"
        if line == "Stage" and current_course_code is not None:
            i += 1
            cat_list = []
            while i < n and (lines[i] in KNOWN_CATEGORIES) and lines[i] not in ["I", "II", "III", "IV"]:
                cat_list.append(lines[i])
                i += 1
                
            # Expect Stage Name (e.g. "I" or "II")
            if i < n and (lines[i] in ["I", "II", "III", "IV"] or re.match(r'^Stage-[I|V]+$', lines[i])):
                stage_code = lines[i].replace("Stage-", "")
                i += 1
                
                # Following are Merit and (Percentile) values for each category in cat_list
                val_idx = 0
                while i < n and val_idx < len(cat_list):
                    # If line is another institute/course header or Stage, stop
                    if re.match(r'^\d{5}\s*-', lines[i]) or re.match(r'^\d{10}\s*-', lines[i]) or lines[i] == "Stage":
                        break
                        
                    merit_val = None
                    pct_val = None
                    
                    if re.match(r'^\d+$', lines[i]):
                        merit_val = int(lines[i])
                        i += 1
                        
                    if i < n:
                        pct_match = re.match(r'^\(?(\d+\.?\d*)\)?$', lines[i])
                        if pct_match:
                            try:
                                pct_val = float(pct_match.group(1))
                                i += 1
                            except ValueError:
                                pass
                                
                    if pct_val is not None and val_idx < len(cat_list):
                        cat_code = cat_list[val_idx]
                        inst_code_val = current_inst_code if current_inst_code else current_course_code[:5]
                        parsed_rows.append({
                            "academic_year": academic_year,
                            "year_num": year_num,
                            "cap_round": cap_round,
                            "seat_type": "MH",
                            "institute_code": inst_code_val,
                            "institute_name": current_inst_name,
                            "institute_status": current_status,
                            "course_code": current_course_code,
                            "branch_name": current_branch_name,
                            "seat_pool": current_pool if current_pool else "State Level",
                            "seat_category_code": cat_code,
                            "stage_code": stage_code,
                            "merit_no": merit_val,
                            "cutoff_percentile": pct_val,
                            "source_file": source_file,
                            "source_page": source_page
                        })
                        val_idx += 1
                    else:
                        break
            continue
            
        i += 1
        
    return parsed_rows

def parse_all_cutoff_tables(interim_csv="dataset/interim/pdf_pages.csv", output_csv="dataset/processed/cutoffs_long.csv"):
    df_pages = pd.read_csv(interim_csv)
    df_cutoffs = df_pages[df_pages["document_type"] == "cutoff"]
    
    all_parsed = []
    print(f"Parsing cutoff tables from {len(df_cutoffs)} pages...")
    for _, row in df_cutoffs.iterrows():
        records = parse_cutoff_page_text(row)
        all_parsed.extend(records)
        
    df_res = pd.DataFrame(all_parsed)
    # Ensure institute_code and institute_name are fully populated
    inst_map = df_res.dropna(subset=['institute_name']).drop_duplicates(subset=['institute_code']).set_index('institute_code')['institute_name'].to_dict()
    df_res['institute_code'] = df_res['institute_code'].fillna(df_res['course_code'].astype(str).str[:5])
    df_res['institute_name'] = df_res['institute_name'].fillna(df_res['institute_code'].map(inst_map))
    
    print(f"Total parsed cutoff rows: {len(df_res)}")
    print(f"Remaining null institute_names: {df_res['institute_name'].isnull().sum()}")
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_res.to_csv(output_csv, index=False)
    print(f"Saved normalized cutoffs to {output_csv}")
    print(df_res.head(5))
    return df_res

if __name__ == "__main__":
    parse_all_cutoff_tables()
