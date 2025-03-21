import os
import camelot

# NOTE: Manually download "https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU20230002518/O/D20232518.pdf" and saved as "source.pdf"
pdf_filename = "source.pdf"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(pdf_filename):
    print(f"File {pdf_filename} not found")
    exit(1)

# Extract tables and save as markdown
for i in range(3, 87):
    tables = camelot.read_pdf(pdf_filename, pages=str(i), flavor='stream')
    if tables:
        tables[0].to_markdown(os.path.join(output_dir, f'page_{i}.md'))
    else:
        print(f'No tables found on page {i}')
