from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('Noto', '', 'NotoSerifBalinese-Regular.otf', uni=True)
        self.set_font('Noto', '', 12)

    def add_paragraph(self, text):
        special_chars = ['\\', ';', '=']

        if any(c in text for c in special_chars):
            # Pakai Helvetica untuk teks dengan karakter Latin yang bermasalah
            self.set_font('Helvetica', '', 12)
        else:
            self.set_font('Natya', '', 12)

        self.multi_cell(0, 8, text, align='J')
        self.ln()

def prepare_paragraphs(text):
    paragraphs = text.strip().split('\n\n')  # Dua newline sebagai pemisah
    return [p.replace('\n', ' ') for p in paragraphs]

with open("output/output_bali.txt", "r") as f:
    raw_text = f.read()

pdf = PDF()
pdf.add_page()

for paragraph in prepare_paragraphs(raw_text):
    pdf.add_paragraph(paragraph)

pdf.output("output.pdf")
