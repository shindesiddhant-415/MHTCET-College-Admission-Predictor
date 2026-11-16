"""
Module: download_pdfs.py
Purpose: Manage official MHT-CET PDF downloads, verify file integrity, and output the source manifest.
"""

import os
import json
import pandas as pd
import requests

def check_or_download_sources(config_path="config/sources.json", output_manifest="docs/source_manifest.csv"):
    with open(config_path, "r") as f:
        config = json.load(f)
        
    records = []
    print("Checking source PDFs against manifest...")
    for src in config["sources"]:
        local_path = src["local_path"]
        exists = os.path.exists(local_path)
        file_size = os.path.getsize(local_path) if exists else 0
        
        status = "Available (Local)" if exists else "Missing"
        
        # If missing, attempt network fetch
        if not exists and src.get("url"):
            try:
                resp = requests.get(src["url"], timeout=10)
                if resp.status_code == 200:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "wb") as f_out:
                        f_out.write(resp.content)
                    status = "Downloaded"
                    file_size = len(resp.content)
                else:
                    status = f"HTTP Error {resp.status_code}"
            except Exception as e:
                status = f"Download Failed: {str(e)[:30]}"
                
        records.append({
            "source_id": src["id"],
            "academic_year": src["academic_year"],
            "year_num": src["year_num"],
            "document_type": src["document_type"],
            "cap_round": src["cap_round"],
            "seat_type": src["seat_type"],
            "file_name": src["file_name"],
            "local_path": local_path,
            "url": src["url"],
            "file_size_bytes": file_size,
            "status": status
        })
        
    df_manifest = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_manifest), exist_ok=True)
    df_manifest.to_csv(output_manifest, index=False)
    print(f"Source manifest successfully saved to {output_manifest}")
    print(df_manifest[["source_id", "academic_year", "document_type", "cap_round", "status", "file_size_bytes"]])
    return df_manifest

if __name__ == "__main__":
    check_or_download_sources()

