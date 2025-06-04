import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.mode_jtwk import mode_normal, mode_sriwedari, mode_cerita, mode_sanskrit, mode_satya, mode_kakawin, mode_lampah
from modul_jtwk.hukum_jtwk import kata_baku, hukum_aksara, hukum_sigeg, hukum_ṙ, finalisasi 
from modul_jtwk.replacements_jtwk import replacements, replace_numbers_with_colon
from modul_jtwk.hukum_kakawin import cek_kakawin
from modul_jtwk.hukum_macapat import cek_macapat
#, debug_metrum_pada_puisi, hitung_jumlah_metrum, aplikasikan_metrum_dan_tandai_vokal #process_baris, 

def replace_characters(text, mode):

    #paksa konsonan jadi huruf kecil kecuali vokal kapital
    def paksa_huruf_kecil(text):
        vokal_kapital = "AĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ"
        return ''.join(
            c if c in vokal_kapital else c.lower()
            for c in text
        )
    text = paksa_huruf_kecil(text)

    #======Mulai transliterasi sesuai file replacements.py=====
    # Pilih set transliterasi sesuai mode
    mode_replacements = replacements.get(mode, replacements)
    # Terapkan transliterasi dasar secara case-insensitive
    for old_char, new_char in mode_replacements.items():
        text = re.sub(re.escape(old_char), new_char, text, flags=re.IGNORECASE)

    #=======Mulai transliterasi mentah========
    #Aplikasikan kata baku terlebih dahulu
    text = kata_baku(text)
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
    if mode in ('sanskrit'):
        text = mode_sanskrit(text)
    if mode in ('satya'):
        text = mode_satya(text)

    # Masukkan hukum r
    text = hukum_ṙ(text) 

    #penghitung metrum/puisi
    if mode in {'kakawin'}:
        text = cek_kakawin(text)
    if mode in {'macapat'}:
        text = cek_macapat(text)

    # Masukkan hukum sigeg
    text = hukum_sigeg(text)

    #=====Modifikasi terakhir====
    # Mengubah angka dengan format angka. menjadi :angka:
    text = replace_numbers_with_colon(text)
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