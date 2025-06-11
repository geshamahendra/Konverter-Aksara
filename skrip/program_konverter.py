import tkinter as tk
from tkinter import scrolledtext
import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
# Pastikan jalur ini benar untuk struktur proyek Anda
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# --- IMPOR MODUL DAN FUNGSI ANDA ---
try:
    from modul_jtwk.aturan_aksara import aksara, sandhangan, simbol, swara
    from modul_jtwk.aturan_aksara import inisialisasi, hukum_sandi, finalisasi, hukum_penulisan
    from modul_jtwk.hukum_jtwk import kata_baku, hukum_aksara, hukum_sigeg, hukum_ṙ, finalisasi_jtwk
    from modul_jtwk.replacements_jtwk import replacements, replace_numbers_with_colon

except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Pastikan folder 'modul_jtwk' ada di direktori yang benar dan berisi file-file yang diperlukan.")

    def inisialisasi(text): return text.lower()
    def hukum_sandi(text): return text
    def hukum_penulisan(text): return text
    def finalisasi(text): return text

# --- Fungsi handle_vokal_khusus Anda ---
def handle_vokal_khusus(char, hasil, last_char, last_aksara):
    vokal_khusus = {
        'ṛ':  ('ꦉ', 'ꦽ', 'ꦽꦴ', swara.get('ṛ', 'ꦉ')),
        'ṝ':  ('ꦉꦴ', 'ꦽꦴ', 'ꦽꦴ', swara.get('ṝ', 'ꦉꦴ')),
        'ḷ':  ('ꦊ', '꧀ꦭꦼ', '꧀ꦭꦼꦴ', swara.get('ḷ', 'ꦊ')),
        'ḹ':  ('ꦋ', '꧀ꦭꦼꦴ', '꧀ꦭꦼꦴ', swara.get('ḹ', 'ꦋ')),
    }
    if char not in vokal_khusus:
        return hasil + char, char

    awal, tengah, panjang, default = vokal_khusus[char]
    if last_aksara and last_aksara.endswith('꧀'):
        return hasil[:-1] + tengah, tengah
    elif last_char in [' ', '\n'] or not last_char:
        return hasil + awal, awal
    else:
        return hasil + default, default

karakter_baku = {
    'ng': 'ṅ',
    'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
    'th': 'ŧ','ṭh': 'ṫ','ḍh': 'ḋ','dh': 'đ',
    'ph': 'ꝑ','bh': 'ƀ',
    'ai': 'ꜽ', 'au': 'ꜷ', 
    #'-' : ' ', 
    'Ç' : 'Ś', 'ç' : 'ś',
    '’' : '0‍',
    '‘' : '0‍',

    "x" : 'ś', "f" : 'ṣ', "t'" : 'ṭ', "d'" : 'ḍ', "q" : 'ĕ', "n`" : 'ñ', "n'" : 'ṇ', "o'" : 'ö', 'v' : 'w',
    #'ṃ' : 'ŋ',  
    'ṁ' : 'ŋ',
    #'sh' : 'ś','ss' : 'ṣ',

    'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ', 'Om̃' : 'Ōṃ',
}

# --- Fungsi latin_to_jawa Anda ---
def latin_to_jawa(text, line_spacing=1):

    #paksa konsonan jadi huruf kecil kecuali vokal kapital
    def paksa_huruf_kecil(text):
        vokal_kapital = "AĀÂIĪÎUŪÛOŌÔĔEÊÉÈꜼꜶ"
        return ''.join(
            c if c in vokal_kapital else c.lower()
            for c in text
        )
    text = paksa_huruf_kecil(text)

    # Terapkan perubahan dari dictionary perubahan_awal_input
    for key, value in karakter_baku.items():
        text = text.replace(key, value)

    #replacement

    #=======Mulai transliterasi mentah========
    #Aplikasikan kata baku terlebih dahulu
    text = kata_baku(text)
    # Tingkat Ketiga: Modifikasi lebih lanjut
    text = hukum_aksara(text)

    # Masukkan hukum r
    text = hukum_ṙ(text) 

    # Masukkan hukum sigeg
    text = hukum_sigeg(text)

    #=====Modifikasi terakhir====
    # Mengubah angka dengan format angka. menjadi :angka:
    text = replace_numbers_with_colon(text)
    #finalisasi
    text = finalisasi_jtwk(text)



    text = inisialisasi(text)
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
            last_aksara = ""
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
                if hasil:
                    hasil = hasil[:-1]
                sand_char = sandhangan[char]
                hasil += sand_char
                last_aksara = last_aksara[:-1] + sand_char
            else:
                hasil += sandhangan[char]
                last_aksara += sandhangan[char]
            last_char = char
            is_new_line = False
            continue

        hasil += char
        last_aksara = ""
        last_char = char
        is_new_line = False

    hasil = finalisasi(hasil)
    hasil = re.sub(r'ꦪꦾꦂ', 'ꦫ꧀ꦪꦾ', hasil)
    hasil = re.sub(r'ꦫ꧀ꦮ', 'ꦫ꧀ꦮ\u200D', hasil)

    #khusus font jayabaya
    hasil = re.sub(r'ꦈ', '#', hasil)
    hasil = re.sub(r'ꦎ', 'ꦈ', hasil)
    hasil = re.sub(r'#', 'ꦎ', hasil)
    
    hasil = re.sub(r'ꦂ', 'ꦂ\u200D', hasil, flags=re.IGNORECASE)
    return hasil

# --- FUNGSI UTAMA UNTUK INTERAKSI GUI ---
conversion_cache = {}

def process_input(event=None):
    current_text = input_text_widget.get("1.0", tk.END).strip()

    if not current_text:
        display_output_jawa("")
        return

    # Konversi seluruh teks input ke Aksara Jawa
    converted_full_text = latin_to_jawa(current_text, line_spacing=1)

    # Hapus semua spasi dari hasil akhir, kecuali jika spasi digunakan sebagai simbol tertentu
    # Jika spasi murni pemisah kata, maka ini yang Anda inginkan.
    # Jika simbol[' '] adalah spasi ' ', maka kita perlu logika yang lebih canggih di latin_to_jawa.
    final_jawa_output = converted_full_text.replace(" ", "") 
    
    # Tampilkan seluruh hasil konversi
    display_output_jawa(final_jawa_output)

def display_output_jawa(text):
    # Hapus konten lama
    output_jawa_widget.config(state=tk.NORMAL) # Atur ke normal untuk edit
    output_jawa_widget.delete("1.0", tk.END)
    # Sisipkan teks baru
    output_jawa_widget.insert("1.0", text)
    output_jawa_widget.config(state=tk.DISABLED) # Atur kembali ke disabled (read-only)

# --- SETUP GUI TKINTER ---
root = tk.Tk()
root.title("Aplikasi Konversi Latin ke Aksara Jawa")

# Membuat PanedWindow sebagai kontainer utama
# orient=tk.VERTICAL akan membuat panel atas dan bawah dengan pembatas horizontal
main_paned_window = tk.PanedWindow(root, orient=tk.VERTICAL, sashrelief=tk.RAISED)
main_paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Isi seluruh jendela

# 1. Frame untuk Panel Output Aksara Jawa (atas)
# Kita perlu Frame untuk menampung Label dan ScrolledText di dalam PanedWindow
output_frame = tk.Frame(main_paned_window)
output_frame.pack(fill=tk.BOTH, expand=True) # Fill the frame

output_jawa_label = tk.Label(output_frame, text="Hasil Aksara Jawa:")
output_jawa_label.pack(anchor=tk.W, pady=(0, 5))

output_jawa_widget = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=10, font=("jayaƀaya", 14))
output_jawa_widget.pack(fill=tk.BOTH, expand=True) # Penting: fill=BOTH dan expand=True
output_jawa_widget.config(state=tk.DISABLED) # Membuatnya read-only

# 2. Frame untuk Panel Input Latin (bawah)
input_frame = tk.Frame(main_paned_window)
input_frame.pack(fill=tk.BOTH, expand=True) # Fill the frame

input_label = tk.Label(input_frame, text="Ketik Teks Latin di sini:")
input_label.pack(anchor=tk.W, pady=(0, 5))

input_text_widget = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
input_text_widget.pack(fill=tk.BOTH, expand=True) # Penting: fill=BOTH dan expand=True
input_text_widget.bind("<KeyRelease>", process_input)

# --- Menambahkan Frame ke PanedWindow ---
# Order matters: output_frame akan di atas, input_frame di bawah
main_paned_window.add(output_frame)
main_paned_window.add(input_frame)

# Opsional: Atur initial sash position (posisi pembatas awal)
# main_paned_window.sash_place(0, 0, 200) # Atur panel atas ke tinggi 200 piksel, panel bawah akan mengisi sisanya

# Menjalankan loop utama aplikasi GUI
root.mainloop()