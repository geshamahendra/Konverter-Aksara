import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

nglegena = {
    'ꦏ': 'क', 'ꦑ': 'ख', 'ꦒ': 'ग', 'ꦓ': 'घ', 'ꦔ': 'ङ', 'ꦲ': 'ह',
    'ꦕ': 'च', 'ꦖ': 'छ', 'ꦗ': 'ज', 'ꦙ': 'झ', 'ꦚ': 'ञ', 'ꦯ': 'श', 'ꦪ': 'य', 
    'ꦛ': 'ट', 'ꦜ': 'ठ', 'ꦝ': 'ड', 'ꦞ': 'ढ', 'ꦟ': 'ण', 'ꦰ': 'ष', 'ꦫ': 'र', 
    'ꦠ': 'त', 'ꦡ': 'थ', 'ꦢ': 'द', 'ꦣ': 'ध', 'ꦤ': 'न', 'ꦱ': 'स', 'ꦭ': 'ल',
    'ꦥ': 'प', 'ꦦ': 'फ', 'ꦧ': 'ब', 'ꦨ': 'भ', 'ꦩ': 'म', 'ꦮ': 'व', 

    'ꦾ': '्य', 'ꦿ': '्र'
}

swara = {
    'ꦄ': 'अ', 'ꦄꦴ': 'आ', 'ꦅ': 'इ', 'ꦆ': 'ई', 'ꦇ': 'ई', 'ꦎ': 'ओ', 'ꦎꦴ': 'औ', 
    'ꦌ': 'ए', 'ꦍ': 'ऐ', 'ꦈ': 'उ', 'ꦈꦴ': 'ऊ', 'ꦉ': 'ऋ', 'ꦉꦴ': 'ॠ', 
    'ꦊ': 'ऌ', 'ꦋ': 'ॡ', 'ꦽ': 'ृ', 'ꦽꦴ': 'ॄ',
}

sandhangan = {
    'ꦴ': 'ा', 'ꦶ': 'ि', 'ꦷ': 'ी', 'ꦸ': 'ु', 'ꦹ': 'ू', 'ꦺ': 'े', 'ꦻ': 'ै', 
    'ꦼ': 'ॅ', 'ꦺꦴ': 'ो', 'ꦻꦴ': 'ौ', 'ꦂ':'र्'
}

sigeg = {
    'ꦀ': 'ँ', 'ꦁ': 'ं', 'ꦂ': 'र्', 'ꦃ': 'ः', '꧀': '्',
}

angka = {
    '꧐': '०', '꧑': '१', '꧒': '२', '꧓': '३', '꧔': '४', '꧕': '५', '꧖': '६', '꧗': '७', '꧘': '८', '꧙': '९',
}

simbol = {
    '꧆': '।', '꧇': '॥', '꧈': ',', '꧉': '.', '꧊': '॰', '꧅': 'ॐ', '꧄': '*', '꧃': 'ऽ', '꧋': '॥', 
    '_': '—', '꧁': '«', '꧂': '»', 
}

# Gabungkan semua kategori menjadi satu dictionary
daftar_konversi = {}
daftar_konversi.update(swara)
daftar_konversi.update(nglegena)
daftar_konversi.update(sandhangan)
daftar_konversi.update(sigeg)
daftar_konversi.update(angka)
daftar_konversi.update(simbol)

def konversi_aksara_ke_kawi(text, daftar_konversi):
    hasil = []
    for karakter in text:
        hasil.append(daftar_konversi.get(karakter, karakter))  # Gunakan karakter asli jika tidak ditemukan
   
    text = ''.join(hasil)
    return text


def process_file(input_file, output_file, daftar_konversi):
    # Membaca isi file input
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    teks_terkonversi = konversi_aksara_ke_kawi(text, daftar_konversi)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(teks_terkonversi)

    print(f"Konversi selesai! Hasil telah disimpan di: {output_file}")

if __name__ == '__main__':
    # Nama file input dan output
    input_file = 'output/output_jawa.txt'  
    output_file = 'output/output_devanagri.txt'  

    # Memproses file
    process_file(input_file, output_file, daftar_konversi)