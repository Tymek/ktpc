import os
import re
from pathlib import Path

def extract_page_number(filename):
    """Extract page number from filename"""
    match = re.search(r'page_(\d+)\.md', filename)
    return int(match.group(1)) if match else float('inf')

def extract_unit_from_header(header):
    """Extract unit from header like fdolna(kHz) or fgorna(GHz)"""
    match = re.search(r'\(([^)]+)\)', header)
    return match.group(1) if match else 'kHz'  # Default to kHz if no unit found

def process_frequency(freq_str, unit):
    if not freq_str or freq_str.strip() == '':
        return freq_str
    
    # Remove any whitespace
    freq_str = freq_str.strip()
    
    # Handle special cases
    if freq_str.lower() == 'poniżej 8,3 khz':
        return 'Below 8.3 kHz'
    
    # If the value already has a unit, return as is
    if any(u in freq_str for u in ['kHz', 'MHz', 'GHz', 'Hz']):
        return freq_str
        
    # Process the numeric part
    number = freq_str.replace(',', '.')
    
    # Add the unit from the header
    return f"{number} {unit}"

def process_page(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the header row (the one with Lp.)
    header_idx = None
    for i, line in enumerate(lines):
        if 'Lp.' in line:
            header_idx = i
            break
    
    if header_idx is None:
        return []
    
    # Extract units from header columns
    header_line = lines[header_idx]
    header_cols = [col.strip() for col in header_line.split('|')]
    
    # Extract units for frequency columns
    fdolna_unit = extract_unit_from_header(header_cols[3] if len(header_cols) > 3 else '')
    fgorna_unit = extract_unit_from_header(header_cols[4] if len(header_cols) > 4 else '')
    
    # Process all rows after the header
    data_rows = []
    for line in lines[header_idx + 2:]:  # Skip header and separator
        if not line.strip():
            continue
        
        # Split the line into columns and ignore the first column (row number)
        cols = [col.strip() for col in line.split('|')]
        if len(cols) < 6:  # Skip malformed lines
            continue
        
        # Process frequency values with their respective units
        fdolna = process_frequency(cols[3].strip(), fdolna_unit)
        fgorna = process_frequency(cols[4].strip(), fgorna_unit)
        
        # Keep only the relevant columns
        row = {
            'lp': cols[2].strip(),
            'fdolna': fdolna,
            'fgorna': fgorna,
            'przeznaczenie': cols[5].strip(),
            'uzycie': cols[6].strip() if len(cols) > 6 else ''
        }
        
        data_rows.append(row)
    
    return data_rows

def main():
    output_dir = Path('output')
    all_data = []
    
    # Get all page files and sort them by page number
    page_files = sorted(
        output_dir.glob('page_*.md'),
        key=lambda x: extract_page_number(x.name)
    )
    
    # Process all page files
    for file_path in page_files:
        try:
            page_data = process_page(file_path)
            if page_data:
                all_data.extend(page_data)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Create the output markdown table
    output = [
        "| Lp. | fdolna | fgórna | Przeznaczenie | Użytkowanie |",
        "|---:|------:|-------:|:--------------|:------------|"
    ]
    
    for row in all_data:
        output.append(
            f"| {row['lp']} | {row['fdolna']} | {row['fgorna']} | "
            f"{row['przeznaczenie']} | {row['uzycie']} |"
        )
    
    # Write the combined output
    with open('combined_bandplan.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Processed {len(all_data)} rows from {len(page_files)} pages")
    print("Output written to combined_bandplan.md")

if __name__ == '__main__':
    main() 