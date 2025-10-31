import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# Daftar aksara dengan tarung panjang
aksara_tarung_panjang = 'ꦥꦔꦭꦛꦧ'
cakra = 'ꦿ'
joiner = '꧀'
tarung_panjang_char = 'ꦵ'
aksara_nglegena = ''.join([
    'ꦏ', 'ꦑ', 'ꦒ', 'ꦓ', 'ꦔ', 'ꦲ',
    'ꦕ', 'ꦖ', 'ꦗ', 'ꦘ', 'ꦙ', 'ꦚ', 'ꦯ', 'ꦪ',
    'ꦛ', 'ꦜ', 'ꦝ', 'ꦞ', 'ꦟ', 'ꦰ', 'ꦫ',
    'ꦠ', 'ꦡ', 'ꦢ', 'ꦣ', 'ꦤ', 'ꦱ', 'ꦭ',
    'ꦥ', 'ꦦ', 'ꦧ', 'ꦨ', 'ꦩ', 'ꦮ',
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
            (?:[{cakra}])*    # Tambahan: Opsional Pengkal/Cakra - BISA BERULANG (jika ꦽ Keret juga dipertimbangkan)
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

RE_LATIN_TO_JAWA = [
    (re.compile(r'ꦫ꧀ꦮ‍‌ꦶ'), 'ꦫ꧀ꦮ‍ꦶ'),
    (re.compile(r'ꦪꦾꦂ'), 'ꦫ꧀ꦪꦾ'),
    (re.compile(r'ꦼꦴ'), 'ꦼꦵ'),
    (re.compile(r'꧄꧐꧄'), '꧅꧐꧅'),
    (re.compile(r'꧁'), '꧄'),
    (re.compile(r'꧂'), '꧄'),
    # khusus font Jayabaya
    (re.compile(r'ꦈ'), '#'),
    (re.compile(r'ꦎ'), 'ꦈ'),
    (re.compile(r'#'), 'ꦎ'),
]

def latin_to_jawa(text, line_spacing):
    """
    Konversi teks Latin hasil transliterasi menjadi Aksara Jawa
    dengan aturan visual dan penyesuaian font Jayabaya.
    """
    # Tahap awal: atur tarung panjang
    text = tarung(text)

    # Terapkan semua regex
    for regex, replacement in RE_LATIN_TO_JAWA:
        text = regex.sub(replacement, text)

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



        