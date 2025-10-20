import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.konstanta import VOKAL_KAPITAL

from modul_jtwk.mode_jtwk import mode_normal, mode_sriwedari, mode_cerita, mode_sanskrit, mode_satya, mode_kakawin, mode_lampah
from modul_jtwk.hukum_jtwk import kata_baku, hukum_aksara, hukum_sigeg, hukum_ṙ, finalisasi_jtwk
from modul_jtwk.replacements_jtwk import replacements, replace_numbers_with_colon
from modul_jtwk.hukum_kakawin import cek_kakawin
from modul_jtwk.hukum_macapat import cek_macapat

def replace_characters(text, mode):
    #paksa konsonan jadi huruf kecil kecuali vokal kapital
    def paksa_huruf_kecil(text):
        return ''.join(
            c if c in VOKAL_KAPITAL else c.lower()
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
    text = finalisasi_jtwk(text)

    return text

def process_file(input_file, output_file):
    chosen_mode = 'lampah' # Default mode
    header_line_content = '' # Untuk menyimpan konten baris pertama jika itu bukan header

    with open(input_file, 'r', encoding='utf-8') as infile:
        # Coba baca hanya baris pertama
        first_line = infile.readline().strip()

        if first_line: # Pastikan baris pertama tidak kosong
            header_match = re.match(r'^\+([a-zA-Z]+?)\+$', first_line)
            if header_match:
                chosen_mode = header_match.group(1).lower()
                print(f"Mode '{chosen_mode}' terdeteksi dari header file.")
                # Baris header akan diganti dengan baris kosong di output
                # Kita tidak perlu menyimpannya sebagai bagian dari konten yang akan diproses
            else:
                # Jika bukan header, baris pertama adalah bagian dari konten yang akan diproses
                print(f"Tidak ada header mode terdeteksi. Menggunakan mode default '{chosen_mode}'.")
                header_line_content = first_line + '\n' # Tambahkan kembali baris pertama ke konten

        # Baca sisa isi file dari posisi kursor saat ini
        # Ini lebih efisien karena tidak membaca ulang baris pertama
        rest_of_file_content = infile.read()

    # Gabungkan baris pertama (jika bukan header) dengan sisa file
    full_content_to_process = header_line_content + rest_of_file_content

    # Proses teks dengan fungsi replace_characters
    modified_text = replace_characters(full_content_to_process, chosen_mode)

    # Tulis hasil ke file output
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Jika header ditemukan, kita ingin baris itu menjadi baris kosong di output.
        # Jika tidak, modified_text sudah berisi baris pertama.
        if chosen_mode != 'normal' and header_line_content == '': # Ini berarti header ditemukan
            outfile.write('\n' + modified_text) # Tambahkan baris kosong di awal
        else:
            outfile.write(modified_text)


# Ganti dengan nama file input dan output sesuai kebutuhan
input_file = 'input.txt'  # Nama file input
output_file = 'output/input_jawa.txt'  # Nama file output

# Memproses file
process_file(input_file, output_file)

print(f'Teks telah diproses dari {input_file} dan hasilnya disimpan di {output_file}.')