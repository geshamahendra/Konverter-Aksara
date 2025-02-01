import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.hukum_jtwk import kata_baku, hukum_aksara, hukum_sigeg, hukum_ṙ
from modul_jtwk.replacements_jtwk import replacements, replace_numbers_with_colon, retain_final_r
from modul_jtwk.mode_jtwk import mode_normal, mode_lampah, mode_sriwedari, mode_modern_lampah, mode_cerita, mode_sanskrit

# Definisi variabel global
daftar_vokal = "aāiīuūeèoōöŏĕꜷꜽ"  # Daftar vokal
vokal_lampah_spesial = "AIU"
vokal_kapital = "AĀIĪUŪEÈOŌÖŎĔꜶꜼ"  # Daftar vokal kapital
vokal_gabungan = "aāiīuūeèoōöŏĕꜷꜽAĀIĪUŪEÈOŌÖŎĔꜶꜼ"
daftar_konsonan = "bdfhjnptvyzḋḍŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"  # Daftar konsonan
daftar_konsonan_sigeg = "ŋḥṃṙ"  # Daftar konsonan
zwnj = '\u200C'  # Zero-width non-joiner (ZWNJ)

def replace_r_or_ṙ_with_r_vokal(text):   
    # Pola untuk mencocokkan 'r' atau 'ṙ' yang diikuti oleh spasi dan vokal
    pattern = r'([ṙr])\s([' + re.escape(daftar_vokal) + r'])'
    
    # Fungsi pengganti untuk menggantikan 'r' atau 'ṙ' dengan 'r' diikuti vokal
    def replace(match):
        return 'r' + match.group(2)

    # Terapkan substitusi pada teks
    return re.sub(pattern, replace, text)


def replace_characters(text, mode):
    # Mengubah set daftar_vokal menjadi string
    vokal_kapital_str = ''.join(vokal_kapital)

    #=====Modifikasi lebih lanjut tentang huruf vokal====
    # Memastikan uppercase vokal tetap utuh dan lowercase tetap lowercase
    text = re.sub(r'[^' + re.escape(vokal_kapital_str) + ']', lambda m: m.group(0).lower() if m.group(0) not in vokal_kapital else m.group(0), text)
    # Mengubah vokal menjadi uppercase jika didahului oleh karakter non-huruf yang bukan spasi
    text = re.sub(rf'(?<=[^\w\s])([{daftar_vokal}])', lambda m: m.group(1).upper(), text)

    #=======Mulai transliterasi mentah========
    #Aplikasikan kata baku terlebih dahulu
    text = kata_baku(text)
    # Mengubah vokal menjadi uppercase hanya jika setelah tanda baca, bukan spasi
    text = re.sub(rf'(?<=[^\w\s])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)
    # Kapitalkan vokal di awal baris
    text = re.sub(rf'^[{daftar_vokal}]', lambda m: m.group(0).upper(), text, flags=re.MULTILINE)
    # Masukkan hukum sigeg
    text = hukum_sigeg(text)

    #======Mulai transliterasi sesuai file replacements.py=====
    # Pilih set transliterasi sesuai mode
    mode_replacements = replacements.get(mode, replacements)
    # Terapkan transliterasi dasar secara case-insensitive
    for old_char, new_char in mode_replacements.items():
        text = re.sub(re.escape(old_char), new_char, text, flags=re.IGNORECASE)

    # Tingkat Ketiga: Modifikasi lebih lanjut
    text = hukum_aksara(text) 
   
    #========Aturan Berdasarkan Mode========
    if mode in {'sriwedari'}:
        text = mode_sriwedari(text)
    if mode in {'normal'}:
        text = mode_normal(text)
    if mode in {'cerita'}:
        text = mode_cerita(text)
    if mode in {'lampah', 'sumanasantaka'}:
        text = mode_lampah(text)
    if mode in ('modern_lampah'):
        text = mode_modern_lampah(text)
    if mode in ('sanskrit'):
        text = mode_sanskrit(text)
        
    # Masukkan hukum r
    text = hukum_ṙ(text)

    #=====Modifikasi terakhir====
    # Mengubah angka dengan format angka. menjadi :angka:
    text = replace_numbers_with_colon(text)
    # Mengubah huruf selain vokal menjadi lowercase
    text = re.sub(r'[^' + re.escape(vokal_kapital_str) + ']', lambda m: m.group(0).lower(), text)
    # Panggil fungsi untuk mempertahankan 'r' di akhir kalimat atau baris
    text = retain_final_r(text)

    #Menghapus tanda backtick setelah proses penggantian selesai
    text = text.replace('`', '')  # Menghapus tanda backtick yang digunakan sementara

    text = re.sub(r'(?<=\b)rakṙyyan(?=\b)', 'rakryan', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)rakṙyyān(?=\b)', 'rakryān', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)ry(?=\b)', 'yyṙ‌', text, flags=re.IGNORECASE)
    #text = re.sub(r'(?<=\b)ṣi(?=\b)', 'rṣi', text, flags=re.IGNORECASE)

    return text


def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()
    modified_text = replace_characters(text, mode)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_text)

# Ganti dengan nama file input dan output sesuai kebutuhan
input_file = 'input.txt'  # Nama file input
output_file = 'output/input_jawa.txt'  # Nama file output
mode = 'sanskrit'

# Memproses file
process_file(input_file, output_file)

print(f'Teks telah diproses dari {input_file} dan hasilnya disimpan di {output_file}.')