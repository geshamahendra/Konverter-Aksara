import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from modul_jtwk.aturan_aksara import aksara, sandhangan, simbol, swara
from modul_jtwk.aturan_aksara import hukum_sandi, finalisasi

def latin_to_jawa(text, line_spacing):
    text = re.sub(r'ṙ', 'r', text, flags=re.IGNORECASE)
    text = hukum_sandi(text)

    # Init
    hasil = ""
    last_aksara = ""  
    last_char = ""    
    is_new_line = True  

    i = 0
    for i, char in enumerate(text):

        if char == ' ' and i > 0 and i < len(text) - 1:
            prev_char = text[i - 1]
            next_char = text[i + 1]
            
        # Memeriksa spasi dan enter untuk pemisahan baris
        if char == '\n':
            hasil += '\n' * line_spacing # Menambahkan baris baru dengan jumlah line spacing
            # Menambahkan spasi untuk line spacing setelah baris baru
            last_char = '\n'  # Menyimpan karakter terakhir sebagai enter
            continue  # Lewati karakter enter

        # Menangani spasi yang diapit konsonan dan vokal
        if char == ' ' and i > 0 and i < len(text) - 1:
            prev_char = text[i - 1]
            next_char = text[i + 1]

            # Memastikan kondisi karakter sebelumnya adalah konsonan dan berikutnya adalah vokal
            if prev_char in aksara and next_char in sandhangan:
                # Hapus pemati di akhir karakter sebelumnya
                hasil = hasil[:-1] + aksara[prev_char][:-1]
                # Tambahkan sandhangan untuk vokal berikutnya tanpa pemati
                hasil += sandhangan[next_char]
                last_char = next_char

                # Menyambungkan konsonan dengan awalan r-<vokal>
            if prev_char in aksara and next_char == 'r':
                hasil = hasil[:-1] + 'ꦿ'
                last_char = 'r'
                continue

        # Jika huruf kapital atau karakter ada di kategori swara, tambahkan sesuai peta konversi
        if char.isupper() and char in swara:
            hasil += swara[char]
            last_aksara = swara[char]  # Menyimpan aksara terakhir
            last_char = char

        elif char in simbol:
            hasil += simbol[char]
            last_aksara = ""  # Reset last aksara karena simbol tidak mempengaruhi
            last_char = char
        
        # Jika karakter ada dalam peta nglegena, tambahkan sesuai peta konversi
        elif char in aksara and char not in ['r', 'y', 'ṛ','ṝ', 'ḷ', 'ḹ']:#, 's', 'ṣ']:
            hasil += aksara[char]
            last_aksara = aksara[char]  # Menyimpan aksara terakhir
            last_char = char  

        # Jika karakter adalah 'r', kita perlu melakukan pemeriksaan tambahan
        elif char == 'r':
            if last_aksara and last_aksara.endswith('꧀'):
                # Jika iya, tambahkan aksara "cakra" (ꦿ)
                hasil = hasil[:-1] + 'ꦿ'  # Cakra = ꦿ
                last_aksara = 'ꦿ'  # Update last aksara menjadi cakra
            else:
                # Jika tidak, tambahkan aksara "ra"
                hasil += aksara['r']
                last_aksara = aksara['r']  # Menyimpan aksara terakhir

        # Jika karakter adalah 'y', kita perlu melakukan pemeriksaan tambahan
        elif char == 'y':
            if last_aksara == 'ꦿ':  # Cek apakah sebelumnya ada cakra
                hasil += 'ꦾ'  # Tambahkan pengkal
                last_aksara = 'ꦿꦾ'  # Update last_aksara
            elif last_aksara and last_aksara.endswith('꧀'):
                # Jika iya, tambahkan aksara "pengkal" (ꦾ)
                hasil = hasil[:-1] + 'ꦾ'  # Pengkal = ꦾ
                last_aksara = 'ꦾ'  # Update last aksara menjadi pengkal 
            else:
                # Jika tidak, tambahkan aksara "ra"
                hasil += aksara['y']
                last_aksara = aksara['y']  # Menyimpan aksara terakhir

        # Jika karakter adalah 'ṛ', kita perlu melakukan pemeriksaan tambahan
        elif char == 'ḷ':
            if last_aksara and last_aksara.endswith('꧀'):
                # Jika iya, tambahkan aksara 
                hasil = hasil[:-1] + '꧀ꦭꦼ'  
                last_aksara = '꧀ꦭꦼ'
            elif last_char == ' ':
                hasil = hasil[:-1] + 'ꦊ'  # Tambahkan ꦉ jika sebelumnya '|'
                last_aksara = 'ꦊ'  # Mengatur aksara terakhir ke ꦉ
            else:
                # Jika tidak, tambahkan aksara "ḷ"
                hasil += swara['ḷ']
                last_aksara = swara['ḷ']  # Menyimpan aksara terakhir 

        # Jika karakter adalah 'ṛ', kita perlu melakukan pemeriksaan tambahan
        elif char == 'ḹ':
            if last_aksara and last_aksara.endswith('꧀'):
                # Jika iya, tambahkan aksara 
                hasil = hasil[:-1] + '꧀ꦭꦼꦴ'  
                last_aksara = '꧀ꦭꦼꦴ'
            elif last_char == ' ':
                hasil = hasil[:-1] + 'ꦋ'  # Tambahkan ꦉ jika sebelumnya '|'
                last_aksara = 'ꦋ'  # Mengatur aksara terakhir ke ꦉ
            else:
                # Jika tidak, tambahkan aksara "ḷ"
                hasil += swara['ḹ']
                last_aksara = swara['ḹ']  # Menyimpan aksara terakhir     

        # Jika karakter adalah 'ṛ', kita perlu melakukan pemeriksaan tambahan
        elif char == 'ṛ':
            if last_aksara and last_aksara.endswith('꧀'):
                # Jika iya, tambahkan aksara 
                hasil = hasil[:-1] + 'ꦽ'  
                last_aksara = 'ꦽ'
            elif last_char == ' ':
                hasil = hasil[:-1] + 'ꦉ'  # Tambahkan ꦉ jika sebelumnya '|'
                last_aksara = 'ꦉ'  # Mengatur aksara terakhir ke ꦉ
            else:
                # Jika tidak, tambahkan aksara "ra"
                hasil += swara['ṛ']
                last_aksara = swara['ṛ']  # Menyimpan aksara terakhir

        # Jika karakter adalah 'ṝ', kita perlu melakukan pemeriksaan tambahan
        elif char == 'ṝ':
            if last_aksara and last_aksara.endswith('꧀'):
                # Jika iya, tambahkan aksara 
                hasil = hasil[:-1] + 'ꦽꦴ'  
                last_aksara = 'ꦽꦴ'
            elif last_char == ' ':
                hasil = hasil[:-1] + 'ꦉꦴ'  # Tambahkan ꦉ jika sebelumnya '|'
                last_aksara = 'ꦉꦴ'  # Mengatur aksara terakhir ke ꦉ
            else:
                # Jika tidak, tambahkan aksara "ra"
                hasil += swara['ṝ']
                last_aksara = swara['ṝ']  # Menyimpan aksara terakhir

        # Jika karakter ada dalam peta sandhangan, tambahkan sesuai peta konversi
        elif char in sandhangan:
            if is_new_line and last_aksara == '':
                sandhangan_char = sandhangan[char].upper()  # Menjadikan sandhangan uppercase
                hasil += sandhangan_char  # Menambahkan sandhangan yang sudah uppercase
                last_aksara = sandhangan_char  # Menyimpan aksara terakhir
                is_new_line = False  # Set flag ke False setelah karakter pertama pada baris 
            # Jika aksara terakhir ada dan ada sandhangan, hapus tanda pemati
            elif last_aksara and last_aksara.endswith('꧀'):  # Memeriksa tanda pemati
                last_aksara = last_aksara[:-1]  # Menghapus tanda pemati
                hasil = hasil[:-1]  # Menghapus aksara terakhir dari hasil
                # Logika untuk uppercase sandhangan jika ada ꧀ sebelumnya
                if char in sandhangan:
                    sandhangan_char = sandhangan[char].upper()  # Menjadikan sandhangan uppercase
                    hasil += sandhangan_char  # Menambahkan sandhangan yang sudah uppercase
                    last_aksara += sandhangan_char  # Update last_aksara dengan sandhangan uppercase
                else:
                    hasil += sandhangan[char]  # Menambahkan sandhangan jika tidak perlu uppercase
                    last_aksara += sandhangan[char]  # Update last_aksara dengan sandhangan
            else:
                # Menambahkan sandhangan biasa jika tidak ada aksara pemati sebelumnya
                hasil += sandhangan[char]
                last_aksara += sandhangan[char]  # Menyimpan aksara terakhir
                last_char = char  # Update last_char

        # Jika karakter tidak ditemukan dalam peta, tambahkan langsung tanpa perubahan
        else:
            hasil += char
            last_aksara = ""  # Reset last aksara karena karakter umum tidak mempengaruhi
            last_char = char  # Update last_char

    #Finalisasi
    hasil = finalisasi(hasil)

    hasil = hasil.replace("~", " ")
    hasil = hasil.replace("_", " ")

    return hasil

def convert_file(input_file, output_file, line_spacing=2):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    converted_text = latin_to_jawa(text, line_spacing)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(converted_text)

if __name__ == "__main__":
    input_file = 'output/input_jawa.txt'  # path file input 
    output_file = 'output/output_jawarepha.txt'  # path file output 
    line_spacing = 1

    convert_file(input_file, output_file, line_spacing)
    print("Konversi selesai. Hasil disimpan di:", output_file)



        