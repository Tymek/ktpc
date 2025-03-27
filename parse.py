import os
import camelot
from PyPDF2 import PdfReader

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

# Read text from pages 88 until the end into `output/notes`
reader = PdfReader(pdf_filename)
notes_text = []

# Extract text from pages 88 onwards
for page_num in range(87, len(reader.pages)):
    page = reader.pages[page_num]
    text = page.extract_text()
    notes_text.append(f"## Page {page_num + 1}\n\n{text}\n")

# Save all notes to a single file
with open(os.path.join(output_dir, 'notes.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(notes_text))

print("Parsing complete! Check the output directory for results.")
