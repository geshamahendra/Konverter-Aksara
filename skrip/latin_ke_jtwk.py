import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.hukum_jtwk import kata_baku, hukum_aksara, hukum_sigeg, hukum_ṙ
from modul_jtwk.replacements_jtwk import replacements, replace_numbers_with_colon, retain_final_r

# Definisi variabel global
daftar_vokal = "aāiīuūeèoōöŏĕꜷꜽ"  # Daftar vokal
vokal_lampah_spesial = "AIU"
vokal_kapital = "AĀIĪUŪEÈOŌÖŎĔꜶꜼ"  # Daftar vokal kapital
daftar_konsonan = "bdfhjnptvyzḋḍŧṭṣñṇṅṛṝḷḹꝁǥꞓƀś"  # Daftar konsonan
daftar_konsonan_sigeg = "ŋḥṃṙ"  # Daftar konsonan
zwnj = '\u200C'  # Zero-width non-joiner (ZWNJ)

def add_h_between_vowels(text):
    # Pola untuk mencocokkan vokal yang didahului oleh karakter selain huruf atau di awal kata
    pattern_non_letter = rf"(^|[^a-zA-Zḋḍŧṭṣñṇṅŋṛṝḷḹꝁǥꞓƀśy])([{daftar_vokal}])"

    # Pola untuk mencocokkan vokal yang berturut-turut di dalam kata
    pattern_consecutive_vowels = rf"([{daftar_vokal}])([{daftar_vokal}])"

    # Fungsi untuk menyisipkan 'h' sebelum vokal jika perlu
    def insert_h(match):
        sebelum_vokal = match.group(1)  # Karakter sebelum vokal
        vokal = match.group(2)  # Vokal yang ditemukan
        
        # Tambahkan 'h' sebelum vokal
        return sebelum_vokal + 'ʰ' + vokal

    # Fungsi untuk menyisipkan 'h' di antara dua vokal berturut-turut
    def insert_h_between_vowels(match):
        vokal_pertama = match.group(1)  # Vokal pertama
        vokal_kedua = match.group(2)    # Vokal kedua
        
        # Tambahkan 'h' di antara kedua vokal
        return vokal_pertama + 'ʰ' + vokal_kedua

    # Terapkan substitusi untuk pola yang mencocokkan vokal yang didahului oleh karakter non-huruf
    text = re.sub(pattern_non_letter, insert_h, text)

    # Terapkan substitusi untuk pola yang mencocokkan vokal berturut-turut di dalam kata
    return re.sub(pattern_consecutive_vowels, insert_h_between_vowels, text)

def insert_zwnj_between_consonants(text):
    pattern = r'([{b-df-hj-np-tv-zḋḍŧṭṣñṇṅŋṛṝḷḹꝁǥꞓƀś}])\s([b-df-hj-np-tv-zḋḍŧṭṣñṇṅŋṛṝḷḹꝁǥꞓƀś])([b-df-hj-np-tv-zḋḍŧṭṣñṇṅŋṛṝḷḹꝁǥꞓƀś])'
    
    # Sisipkan ZWNJ setelah konsonan pertama (sebelum spasi)
    zwnj = '\u200C'
    
    # Fungsi pengganti untuk memastikan hanya "r" yang dikecualikan jika berada di konsonan ketiga
    def replace_consonants(match):
        first_consonant = match.group(1)
        second_consonant = match.group(2)
        third_consonant = match.group(3)

        # Jika konsonan ketiga adalah "r", jangan tambahkan ZWNJ setelah konsonan pertama
        if third_consonant == 'r':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif first_consonant == 'r':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif third_consonant == 'y':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif first_consonant == 'y':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif third_consonant == 'w':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif first_consonant == 'w':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif third_consonant == 'ṛ':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif first_consonant == 'ṛ':
            return first_consonant + ' ' + second_consonant + third_consonant        
        elif third_consonant == 'ṝ':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif first_consonant == 'ṝ':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif third_consonant == 'l':
            return first_consonant + ' ' + second_consonant + third_consonant
        elif first_consonant == 'l':
            return first_consonant + ' ' + second_consonant + third_consonant                  
        else:
            # Tambahkan ZWNJ antara konsonan pertama dan kedua
            return first_consonant + zwnj + ' ' + second_consonant + third_consonant

    # Terapkan pengganti pada teks
    return re.sub(pattern, replace_consonants, text)

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
   
    # Aturan khusus untuk mode Sriwedari atau jawa
    if mode in {'sriwedari', 'cerita'}:
         # Insert ZWNJ between consecutive consonants
        text = insert_zwnj_between_consonants(text)
        # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
        text = add_h_between_vowels(text)
        print(text)
        # Aturan khusus untuk mode "normal"
    if mode in {'normal'}:
        # Mengubah vokal menjadi uppercase jika didahului oleh spasi dan vokal, tanpa menghapus spasi tersebut
        text = re.sub(rf'(?<=\b[{daftar_vokal}])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)
        # Mengubah vokal pertama setelah spasi menjadi uppercase jika didahului oleh spasi
        text = re.sub(rf'(?<=\s)([{daftar_vokal}])', lambda m: m.group(1).upper(), text)
        # Menghapus spasi sebelum vokal jika didahului oleh konsonan
        text = re.sub(rf'(?<=[^{daftar_vokal}])\s([{daftar_vokal}])', r'\1', text)

        # ZWNJ character (zero-width non-joiner)
        zwnj = '\u200B'
        # Inserting ZWNJ after the consonant if followed by space and capital vowel
        if mode in {'normal'}:
            text = re.sub(rf'([{daftar_konsonan}])(\s)([{vokal_kapital}])', r'\1' + zwnj + r'\2\3', text)

     #Aturan khusus mode lampah
    if mode in {'lampah', 'sumanasantaka'}:
        # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf dan spasi
        text = re.sub(rf'([^\w\s])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2) + m.group(3).upper(), text)

        # Kapitalkan vokal di awal baris
        text = re.sub(rf'(^|\n)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)

        # Aturan baru: menambahkan '/' sebelum spasi jika diapit oleh konsonan di kiri dan vokal uppercase di kanan
        text = re.sub(r'([{daftar_konsonan}])\s([AIUĀĪŪEOÖŎĔÈ])', r'\1/ \2', text)
        
        #text = replace_r_or_ṙ_with_r_vokal(text)
        #khusus sumanasantaka, urai vokal kapital yang didahuli spasi+konsonan
        #text = re.sub(
        #    rf"([{daftar_konsonan}]) ([{vokal_lampah_spesial}])",  # Digunakan untuk mencari huruf konsonan kecil dan vokal kapital AIU
        #    lambda match: match.group(1) + match.group(2).lower() + " " + match.group(2).lower(),
        #    text
        #)

        text=insert_zwnj_between_consonants(text)
        
        #Perubahan pada rṇn
        text = re.sub(r'kw I', 'kwi i', text, flags=re.IGNORECASE)
        text = re.sub(r'rṇ', 'rn', text, flags=re.IGNORECASE)
        
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
    #text = re.sub(r'(?<=\b)ṣi(?=\b)', 'rṣi', text, flags=re.IGNORECASE)

    return text


def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()
    modified_text = replace_characters(text, mode)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_text)

# Ganti dengan nama file input dan output sesuai kebutuhan
input_file = 'input_jtwk.txt'  # Nama file input
output_file = 'output/input_jawa.txt'  # Nama file output
mode = 'sumanasantaka'

# Memproses file
process_file(input_file, output_file)

print(f'Teks telah diproses dari {input_file} dan hasilnya disimpan di {output_file}.')