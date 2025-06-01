import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# Daftar aksara dengan tarung panjang
aksara_tarung_panjang = 'ꦥꦔꦭꦛꦧ'
joiner = '꧀'
tarung_panjang_char = 'ꦵ'
aksara_nglegena = ''.join([
    'ꦏ', 'ꦑ', 'ꦒ', 'ꦓ', 'ꦔ', 'ꦲ',
    'ꦕ', 'ꦖ', 'ꦗ', 'ꦘ', 'ꦙ', 'ꦚ', 'ꦯ', 'ꦪ',
    'ꦛ', 'ꦜ', 'ꦝ', 'ꦞ', 'ꦟ', 'ꦰ', 'ꦫ',
    'ꦠ', 'ꦡ', 'ꦢ', 'ꦣ', 'ꦤ', 'ꦱ', 'ꦭ',
    'ꦥ', 'ꦦ', 'ꦧ', 'ꦨ', 'ꦩ', 'ꦮ'
])
taling_1 = 'ꦺ'
taling_2 = 'ꦻ'
taling_pepet = ('ꦺ', 'ꦻ', 'ꦼ')

def tarung(text):
    # Gabungkan semua pola ke dalam satu regex
    taling_group = '|'.join(taling_pepet)  # Membuat grup untuk taling
    regex = rf'''
        (                           # Grup 1: Bagian sebelum tarung pendek
            [{aksara_tarung_panjang}]       # Aksara tarung panjang
            (?:{joiner}[{aksara_nglegena}])*  # Kombinasi joiner + nglegena (bisa berulang)
            (?:{taling_group})?             # Opsional: salah satu taling
        )
        ꦴ                            # Tarung pendek yang akan diubah
    '''
    # Terapkan regex
    text = re.sub(
        regex,
        lambda m: f"{m.group(1)}{tarung_panjang_char}",
        text,
        flags=re.VERBOSE  # Memungkinkan regex multiline untuk keterbacaan
    )
    return text

def latin_to_jawa(text, line_spacing):
    
    # Terapkan aturan tarung panjang
    text = tarung(text)
    text = re.sub(r'ꦪꦾꦂ', 'ꦫ꧀ꦪꦾ', text)
    text = re.sub(r'ꦫꦾ', '꧟', text)
    text = re.sub(r'ꦫ꧀ꦮ\u200c', '꧞', text)
    text = re.sub(r'ꦾ', '꧀ꦪ', text)
    text = re.sub(r'ꦿ', '꧀ꦫ', text)
    text = re.sub(r'ꦂ', 'ꦂ', text, flags=re.IGNORECASE)#layar ke layar

    '''
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
    '''
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



        