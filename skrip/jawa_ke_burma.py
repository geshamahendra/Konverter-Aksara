import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

daftar_konversi = {
    #nglegena
    'ꦏ': 'က', 'ꦑ': 'ခ', 'ꦒ': 'ဂ', 'ꦓ': 'ဃ', 'ꦔ': 'င', 'ꦲ': 'ဟ',
    'ꦕ': 'စ', 'ꦖ': 'ဆ', 'ꦗ': 'ဇ', 'ꦘ': 'ဉ်', 'ꦙ': 'ဈ', 'ꦚ': 'ည', 'ꦯ': 'ၐ', 'ꦪ': 'ယ', 
    'ꦛ': 'ဋ', 'ꦜ': 'ဌ', 'ꦝ': 'ဍ', 'ꦞ': 'ဎ', 'ꦟ': 'ဏ', 'ꦰ': 'ၑ', 'ꦫ': 'ရ', 
    'ꦠ': 'တ', 'ꦡ': 'ထ', 'ꦢ': 'ဒ', 'ꦣ': 'ဓ', 'ꦤ': 'န', 'ꦱ': 'သ', 'ꦭ': 'လ',
    'ꦥ': 'ပ', 'ꦦ': 'ဖ', 'ꦧ': 'ဗ', 'ꦨ': 'ဘ', 'ꦩ': 'မ', 'ꦮ': 'ဝ', 

     'ꦾ': 'ျ', 'ꦿ': 'ြ',
    
    #swara
    'ꦄ': 'အ', 'ꦄꦴ': 'အာ', 'ꦅ': 'ဣ', 'ꦆ': 'ဤ', 'ꦇ': 'ဤ', 'ꦎ': 'ဥ', 'ꦈꦴ': 'ဦ', 'ꦌ': 'ဧ', 'ꦍ': 'ဨ', 'ꦈ': 'ဩ', 'ꦈꦴ': 'ဪ', 
    
    
    'ꦉ': 'ၒ', 'ꦉꦴ': 'ၓ', 'ꦊ': 'ၔ', 'ꦋ': 'ၕ',
    'ꦽ': 'ၖ', 'ꦽꦴ': 'ၗ', '꧀ꦭꦼ': 'ၘ', '꧀ꦭꦼꦴ': 'ၙ', '꧀ꦊ': 'ၘ', '꧀ꦋ': 'ၙ',

    #sandhangan
    'ꦴ': 'ာ', 'ꦶ': 'ိ', 'ꦷ': 'ီ', 'ꦸ': 'ု', 'ꦹ': 'ူ', 'ꦼ': 'ဵ', 'ꦼꦴ': 'ဵာ', 'ꦺ': 'ေ', 'ꦂ': 'ဲ', 'ꦺꦴ': 'ော', 'ꦻꦴ': 'ေါ်', 
    
    #sigeg
    'ꦀ': 'ᬁ', 'ꦁ': 'ံ', 'ꦃ': 'း', '꦳': '᬴', '꧀': '္', '꧀‌': '်', #'ꦂ': 'ရ်'
    
    #Angka
    '꧑': '၁', '꧒': '၂', '꧓': '၃', '꧔': '၄', '꧕': '၅', '꧖': '၆', '꧗': '၇', '꧘': '၈', '꧙': '၉', '꧐': '၀', 

    #Simbol
    '꧆': '၀', '꧇': ':', '꧈': '၊', '꧉': '။', '꧊': '၎', '꧅': '၏', '꧄': '၌', '꧃': '၍', '꧋': '᭽', '꧁': '᭛᭜᭛', '꧂': '᭛᭜᭛',
    '꧌' : '(', '꧍' : ')' 
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
    output_file = 'output/output_burma.txt' 

    # Memproses file
    process_file(input_file, output_file, daftar_konversi)