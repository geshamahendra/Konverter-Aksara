import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# Kamus konversi karakter spesial ke latin
DAFTAR_KONVERSI = {
    'ꝁ': 'kh', 'Ꝁ': 'Kh',
    'ǥ': 'gh', 'Ǥ': 'Gh',
    'ꞓ': 'ch', 'Ꞓ': 'Ch',
    'ɉ': 'jh', 'Ɉ': 'Jh',
    'ṫ': 'ṭh', 'Ṫ': 'Ṭh',
    'ḋ': 'ḍh', 'Ḋ': 'Ḍh',
    'ŧ': 'th', 'Ŧ': 'Th',
    'đ': 'dh', 'Đ': 'Dh',
    'ꝑ': 'ph', 'Ꝑ': 'Ph',
    'ƀ': 'bh', 'Ƀ': 'Bh',
    'ṛ': 'rĕ', r'ṝ': 'rö',
    'ḷ': 'lĕ', r'ḹ': 'lö',
}

# Konversi karakter spesial ke latin
def konversi_aksara_ke_latin(text, daftar_konversi):
    return ''.join(daftar_konversi.get(kar, kar) for kar in text)

# Ganti vokal ganda dengan bentuk panjang
def ganti_vokal_panjang(text):
    pola_vokal = {
        r'aa': 'ā', r'AA': 'Ā',
        r'ii': 'ī', r'II': 'Ī',
        r'uu': 'ū', r'UU': 'Ū',
    }
    for pola, ganti in pola_vokal.items():
        text = re.sub(pola, ganti, text)
    return text

# Ganti ṙ diikuti 1–2 konsonan jadi r + konsonan-konsonan itu
def ganti_hukum_r(text):

    #kasus re
    text = re.sub(r'ṛĕ', 'rĕ', text)
    text = re.sub(r'(?<!ĕ)ṛ', 'rĕ', text)

    text = re.sub(r'â', 'a a', text, flags=re.IGNORECASE)
    text = re.sub(r'î', 'i i', text, flags=re.IGNORECASE)
    text = re.sub(r'ê', 'a i', text, flags=re.IGNORECASE)
    text = re.sub(r'û', 'u u', text, flags=re.IGNORECASE)
    text = re.sub(r'ô', 'a u', text, flags=re.IGNORECASE)


    return text


def gabungkan_kata_ulang(text):
    # Aturan 1: kata yang persis sama → kuwuŋ kuwuŋ → kuwuŋ-kuwuŋ
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1-\1', text)

    # Aturan 2: kata pertama diakhiri kata kedua → mangadep adep → mangadep-adep
    text = re.sub(r'\b(\w+)\s+(\w+)\b', lambda m:
                  f"{m.group(1)}-{m.group(2)}"
                  if m.group(1).endswith(m.group(2)) else m.group(0), text)

    # Aturan 3: kata kedua diawali kata pertama → raga ragan → raga-ragan
    # Panjang kata kedua harus lebih panjang dari pertama
    text = re.sub(r'\b(\w+)\s+(\w+)\b', lambda m:
                  f"{m.group(1)}-{m.group(2)}"
                  if m.group(2).startswith(m.group(1)) and len(m.group(2)) > len(m.group(1))
                  else m.group(0), text)

    return text

# Proses lengkap file input → output
def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    # Langkah-langkah konversi
    text = konversi_aksara_ke_latin(text, DAFTAR_KONVERSI)
    #text = ganti_vokal_panjang(text)
    #text = gabungkan_kata_ulang(text)
    #text = ganti_hukum_r(text)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(text)

    print(f"Konversi selesai! Hasil disimpan di: {output_file}")

# Jalankan jika file ini dijalankan langsung
if __name__ == '__main__':
    input_file = 'output/input_jawa.txt'
    output_file = 'output/output_latin_normal.txt'
    process_file(input_file, output_file)
