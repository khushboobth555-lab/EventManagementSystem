import os
from fpdf import FPDF

# Set the root directory for your project
ROOT_DIR = r"C:\Users\Karan\OneDrive\Desktop\MCS_Project\EMS"
OUTPUT_PDF = os.path.join(ROOT_DIR, "EMS_Code_Files.pdf")

# File extensions to include
EXTENSIONS = ['.py', '.html', '.js']

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Project Source Files', 0, 1, 'C')
        self.ln(5)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(2)
    def chapter_body(self, body):
        self.set_font('Courier', '', 10)
        # Safely encode to latin1, replacing unsupported chars with '?'
        safe_body = body.encode('latin1', 'replace').decode('latin1')
        self.multi_cell(0, 5, safe_body)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number starts from 78
        page_num = self.page_no() + 77
        self.cell(0, 10, f'{page_num}', 0, 0, 'C')

def collect_files(root_dir, extensions):
    file_list = []
    for folder, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(folder, file))
    return file_list

def main():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    files = collect_files(ROOT_DIR, EXTENSIONS)
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        rel_path = os.path.relpath(file_path, ROOT_DIR)
        pdf.add_page()
        pdf.chapter_title(rel_path)
        pdf.chapter_body(content)
    pdf.output(OUTPUT_PDF)
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
