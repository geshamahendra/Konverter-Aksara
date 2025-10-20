import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

RE_LATIN_TO_JAWA = [
    # Reorder ligatur dasar
    (re.compile(r'ꦪꦾꦂ'), 'ꦫ꧀ꦪꦾ'),
    (re.compile(r'ꦫ꧀ꦮ'), 'ꦫ꧀ꦮ\u200D'),

    # Khusus font Jayabaya (swap ꦈ / ꦎ)
    (re.compile(r'ꦈ'), '#'),
    (re.compile(r'ꦎ'), 'ꦈ'),
    (re.compile(r'#'), 'ꦎ'),

    # Layar ke ra pangku
    (re.compile(r'ꦂ', re.IGNORECASE), 'ꦫ꧀'),
]

def latin_to_jawa(text, line_spacing):
    """Konversi pola Latin ke Aksara Jawa (dengan optimasi regex precompiled)."""
    for regex, repl in RE_LATIN_TO_JAWA:
        text = regex.sub(repl, text)
    return text

def convert_file(input_file, output_file, line_spacing=2):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    converted_text = latin_to_jawa(text, line_spacing)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(converted_text)

if __name__ == "__main__":
    input_file = 'output/output_jawa.txt'  # path file input 
    output_file = 'output/output_jawarepha.txt'  # path file output 
    line_spacing = 1

    convert_file(input_file, output_file, line_spacing)
    print("Konversi selesai. Hasil disimpan di:", output_file)



        