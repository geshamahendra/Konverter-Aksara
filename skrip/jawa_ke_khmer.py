import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

daftar_konversi = {
    #nglegena
    'ꦏ': 'ក', 'ꦑ': 'ខ', 'ꦒ': 'គ', 'ꦓ': 'ឃ', 'ꦔ': 'ង', 'ꦲ': 'ហ',
    'ꦕ': 'ច', 'ꦖ': 'ឆ', 'ꦗ': 'ជ', 'ꦘ': 'ញ', 'ꦙ': 'ឈ', 'ꦚ': 'ណ', 'ꦯ': 'ឝ', 'ꦪ': 'យ', 
    'ꦛ': 'ឋ', 'ꦜ': 'ឌ', 'ꦝ': 'ឍ', 'ꦞ': 'ណ', 'ꦟ': 'ណ', 'ꦰ': 'ឞ', 'ꦫ': 'រ', 
    'ꦠ': 'ត', 'ꦡ': 'ថ', 'ꦢ': 'ដ', 'ꦣ': 'ឬ', 'ꦤ': 'ន', 'ꦱ': 'ស', 'ꦭ': 'ល',
    'ꦥ': 'ប', 'ꦦ': 'ផ', 'ꦧ': 'ព', 'ꦨ': 'ភ', 'ꦩ': 'ម', 'ꦮ': 'វ', 

    'ꦾ': '្យ', 'ꦿ': '្រ',
    
    #swara
    'ꦄ': 'អ', 'ꦄꦴ': 'អា', 'ꦅ': 'ឥ', 'ꦆ': 'ឦ', 'ꦇ': 'ឧ', 'ꦎ': 'ឩ', 'ꦈꦴ': 'ឪ', 'ꦌ': 'ឱ', 'ꦍ': 'ឲ', 'ꦈ': 'ឳ',
    
    'ꦉ': 'ឭ', 'ꦉꦴ': 'ឮ', 'ꦊ': 'ឯ', 'ꦋ': 'ឰ',
    
    #sandhangan
    'ꦴ': 'ា', 'ꦶ': 'ិ', 'ꦷ': 'ី', 'ꦸ': 'ុ', 'ꦹ': 'ូ', 'ꦼ': 'េ', 'ꦼꦴ': 'ែ', 'ꦺ': 'ៃ', 'ꦻ': 'ោ', 'ꦺꦴ': 'ៅ',
    
    #sigeg
    'ꦀ': 'ំ', 'ꦁ': 'ំ', 'ꦂ': '់', 'ꦃ': '៍', '꦳': '៝', '꧀': '្',
    
    #Angka
    '꧑': '១', '꧒': '២', '꧓': '៣', '꧔': '៤', '꧕': '៥', '꧖': '៦', '꧗': '៧', '꧘': '៨', '꧙': '៩', '꧐': '០',
    
    #Simbol
    '꧆': '០', '꧇': ':', '꧈': '។', '꧉': '៕', '꧊': '៛', '꧅': '៖', '꧄': '៚', '꧃': '៙', '꧋': '៎', '꧁': '«', '꧂': '»',
    '꧌': '(', '꧍': ')'
}

def retain_final_asat(text):
    # Tambahkan simbol khusus yang perlu diperhatikan di akhir
    special_symbols = '၊။၌၍၎၏:?()[]'
    pattern = rf'္(?=$|[{re.escape(special_symbols)}])'  
    
    lines = text.splitlines()
    for i, line in enumerate(lines):
        lines[i] = re.sub(pattern, '်', line)  
    
    return "\n".join(lines)

def konversi_aksara_ke_burma(teks, daftar_konversi):
    hasil = []
    for karakter in teks:
        hasil.append(daftar_konversi.get(karakter, karakter))  # Gunakan karakter asli jika tidak ditemukan
    text = ''.join(hasil)
    
    text = re.sub(r'္ဝ', 'ွ', text, flags=re.IGNORECASE)
    text = retain_final_asat(text)
    return text
    

def process_file(input_file, output_file, daftar_konversi):
    with open(input_file, 'r', encoding='utf-8') as infile:
        teks = infile.read()

    teks_terkonversi = konversi_aksara_ke_burma(teks, daftar_konversi)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(teks_terkonversi)

    print(f"Konversi selesai! Hasil telah disimpan di: {output_file}")

if __name__ == '__main__':
    # Nama file input dan output
    input_file = 'output/output_jawa.txt'  
    output_file = 'output/output_khmer.txt' 

    # Memproses file
    process_file(input_file, output_file, daftar_konversi)