import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.hukum_jtwk import kata_baku, hukum_aksara, hukum_sigeg, hukum_ṙ, finalisasi 
from modul_jtwk.replacements_jtwk import replacements, replace_numbers_with_colon, tandai_vokal_pendek_dalam_pasangan, hitung_jumlah_metrum #process_baris, 
from modul_jtwk.mode_jtwk import mode_normal, mode_lampah, mode_sriwedari, mode_modern_lampah, mode_cerita, mode_sanskrit, mode_satya, mode_kakawin

def replace_characters(text, mode):

    #======Mulai transliterasi sesuai file replacements.py=====
    # Pilih set transliterasi sesuai mode
    mode_replacements = replacements.get(mode, replacements)
    # Terapkan transliterasi dasar secara case-insensitive
    for old_char, new_char in mode_replacements.items():
        text = re.sub(re.escape(old_char), new_char, text, flags=re.IGNORECASE)

    #paksa jadi huruf kecil
    text = re.sub(r'(?<!\u200C)([A-Z])', lambda m: m.group(1).lower(), text)

    #=====Modifikasi lebih lanjut tentang huruf vokal====
    daftar_vokal = "aāâiīîuūûeèéêoōöŏôĕꜷꜽ"  # Daftar vokal
    zwnj = '\u200C'  # Zero-width non-joiner (ZWNJ)
    kapitalisasi_khusus = {'ꜽ': 'Ꜽ'}
    # Kapitalkan vokal di awal baris
    text = re.sub(
    rf'^([{daftar_vokal}])',lambda m: kapitalisasi_khusus.get(m.group(1), m.group(1).upper()),text,flags=re.MULTILINE)
    # Menyisipkan ZWNJ dan mengkapitalkan vokal jika didahului tanda baca non-huruf (bukan spasi/strip)
    text = re.sub(rf'([^\w\s-])(\s*)([{daftar_vokal}])',lambda m: f"{m.group(1)}{m.group(2)}{zwnj}{m.group(3).upper()}",text)

    #=======Mulai transliterasi mentah========
    #Aplikasikan kata baku terlebih dahulu
    text = kata_baku(text)
    # Masukkan hukum sigeg
    text = hukum_sigeg(text)
    # Tingkat Ketiga: Modifikasi lebih lanjut
    text = hukum_aksara(text) 
   
    #========Aturan Berdasarkan Mode========
    if mode in {'sriwedari'}:
        text = mode_sriwedari(text)
    if mode in {'normal'}:
        text = mode_normal(text)
    if mode in {'cerita'}:
        text = mode_cerita(text)
    if mode in {'lampah'}:
        text = mode_lampah(text)
    if mode in {'kakawin'}:
        text = mode_kakawin(text)
    if mode in ('modern_lampah'):
        text = mode_modern_lampah(text)
    if mode in ('sanskrit'):
        text = mode_sanskrit(text)
    if mode in ('satya'):
        text = mode_satya(text)
        
    # Masukkan hukum r
    text = hukum_ṙ(text)

    #=====Modifikasi terakhir====
    # Mengubah angka dengan format angka. menjadi :angka:
    text = replace_numbers_with_colon(text)
    #Baris metrum
    #text = "\n".join(process_baris(baris) for baris in text.splitlines())
    text = tandai_vokal_pendek_dalam_pasangan(text)
    #finalisasi
    text = finalisasi(text)

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
mode = 'kakawin'

# Memproses file
process_file(input_file, output_file)

print(f'Teks telah diproses dari {input_file} dan hasilnya disimpan di {output_file}.')