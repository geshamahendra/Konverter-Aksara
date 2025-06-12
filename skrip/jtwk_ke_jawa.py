import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.aturan_aksara import aksara, sandhangan, simbol, swara
from modul_jtwk.aturan_aksara import inisialisasi_aksara, hukum_sandi, finalisasi, hukum_penulisan


def handle_vokal_khusus(char, hasil, last_char, last_aksara):
    # Mapping untuk kasus khusus
    vokal_khusus = {
        'ṛ':  ('ꦉ', 'ꦽ', 'ꦽꦴ', swara['ṛ']),
        'ṝ':  ('ꦉꦴ', 'ꦽꦴ', 'ꦽꦴ', swara['ṝ']),
        'ḷ':  ('ꦊ', '꧀ꦭꦼ', '꧀ꦭꦼꦴ', swara['ḷ']),
        'ḹ':  ('ꦋ', '꧀ꦭꦼꦴ', '꧀ꦭꦼꦴ', swara['ḹ']),
    }

    awal, tengah, panjang, default = vokal_khusus[char]

    if last_aksara and last_aksara.endswith('꧀'):
        return hasil[:-1] + tengah, tengah
    elif last_char in [' ', '\n']:  # ubah ini!
        return hasil + awal, awal
    else:
        return hasil + default, default


def latin_to_jawa(text, line_spacing):
    text = inisialisasi_aksara(text)
    text = hukum_sandi(text)
    text = hukum_penulisan(text)

    hasil = ""
    last_aksara = ""
    last_char = ""
    is_new_line = True

    for i, char in enumerate(text):

        if char == '\n':
            hasil += '\n' * line_spacing
            is_new_line = True
            last_char = '\n'
            last_aksara = ""  # Tambahkan ini!
            continue

        if char == ' ' and i > 0 and i < len(text) - 1:
            prev_char = text[i - 1]
            next_char = text[i + 1]
            if prev_char in aksara and next_char in sandhangan:
                hasil = hasil[:-1] + aksara[prev_char][:-1] + sandhangan[next_char]
                last_char = next_char
                continue

        if char in ['ṛ', 'ṝ', 'ḷ', 'ḹ']:
            hasil, last_aksara = handle_vokal_khusus(char, hasil, last_char, last_aksara)
            last_char = char
            continue

        if char.isupper() and char in swara:
            hasil += swara[char]
            last_aksara = swara[char]
            last_char = char
            is_new_line = False
            continue

        if char in simbol:
            hasil += simbol[char]
            last_aksara = ""
            last_char = char
            is_new_line = False
            continue

        if char in aksara:
            hasil += aksara[char]
            last_aksara = aksara[char]
            last_char = char
            is_new_line = False
            continue

        if char in sandhangan:
            if is_new_line and not last_aksara:
                hasil += sandhangan[char].upper()
                last_aksara = sandhangan[char].upper()
            elif last_aksara and last_aksara.endswith('꧀'):
                hasil = hasil[:-1]
                sand_char = sandhangan[char].upper()
                hasil += sand_char
                last_aksara = last_aksara[:-1] + sand_char
            else:
                hasil += sandhangan[char]
                last_aksara += sandhangan[char]
            last_char = char
            is_new_line = False
            continue

        # Karakter umum lain
        hasil += char
        last_aksara = ""
        last_char = char
        is_new_line = False

    # Finalisasi
    hasil = finalisasi(hasil)
    return hasil


def convert_file(input_file, output_file, line_spacing=2):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    converted_text = latin_to_jawa(text, line_spacing)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(converted_text)


if __name__ == "__main__":
    input_file = 'output/input_jawa.txt'  # Ganti dengan path file input Anda
    output_file = 'output/output_jawa.txt'  # Ganti dengan path file output yang diinginkan
    line_spacing = 1

    convert_file(input_file, output_file, line_spacing)
    print("Konversi selesai. Hasil disimpan di:", output_file)
