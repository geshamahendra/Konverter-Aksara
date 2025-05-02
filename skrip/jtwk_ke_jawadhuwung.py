import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.aturan_aksara import aksara, sandhangan, simbol, swara

def latin_to_jawa(text, line_spacing):
    #text = re.sub(r'ṙ', 'r\u200D', text, flags=re.IGNORECASE)
    text = re.sub(r'ꦪꦾꦂ', 'ꦫ꧀ꦪꦾ', text)
    
    text = re.sub(r'ꦂ', 'ꦫ꧀\u200D', text, flags=re.IGNORECASE)
    text = re.sub(r'꧀ꦧ', '꧀\u200Dꦧ', text, flags=re.IGNORECASE)
    text = re.sub(r'꧀ꦨ', '꧀ꦧ', text, flags=re.IGNORECASE)
    text = re.sub(r'꧀ꦚ', '꧀\u200Dꦚ', text, flags=re.IGNORECASE)

    # Penukaran karakter ꧀ꦱ ↔ ꧀ꦰ tanpa saling menimpa
    text = re.sub(r'꧀ꦱ', '__TEMP_SWAP__', text, flags=re.IGNORECASE)
    text = re.sub(r'꧀ꦰ', '꧀ꦱ', text, flags=re.IGNORECASE)
    text = re.sub(r'__TEMP_SWAP__', '꧀ꦰ', text)
    return text

def convert_file(input_file, output_file, line_spacing=2):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    converted_text = latin_to_jawa(text, line_spacing)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(converted_text)

if __name__ == "__main__":
    input_file = 'output/output_jawa.txt'  # path file input 
    output_file = 'output/output_jawadhuwung.txt'  # path file output 
    line_spacing = 1

    convert_file(input_file, output_file, line_spacing)
    print("Konversi selesai. Hasil disimpan di:", output_file)



        