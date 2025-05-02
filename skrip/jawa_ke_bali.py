import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

daftar_konversi = {
    #nglegena
    'ꦏ': 'ᬓ', 'ꦑ': 'ᬔ', 'ꦒ': 'ᬕ', 'ꦓ': 'ᬖ', 'ꦔ': 'ᬗ', 'ꦲ': 'ᬳ',
    'ꦕ': 'ᬘ', 'ꦖ': 'ᬙ', 'ꦗ': 'ᬚ', 'ꦘ': 'ᭌ', 'ꦙ': 'ᬛ', 'ꦚ': 'ᬜ', 'ꦯ': 'ᬰ', 'ꦪ': 'ᬬ', 
    'ꦛ': 'ᬝ', 'ꦜ': 'ᬞ', 'ꦝ': 'ᬟ', 'ꦞ': 'ᬠ', 'ꦟ': 'ᬡ', 'ꦰ': 'ᬱ', 'ꦫ': 'ᬭ', 
    'ꦠ': 'ᬢ', 'ꦡ': 'ᬣ', 'ꦢ': 'ᬤ', 'ꦣ': 'ᬥ', 'ꦤ': 'ᬦ', 'ꦱ': 'ᬲ', 'ꦭ': 'ᬮ',
    'ꦥ': 'ᬧ', 'ꦦ': 'ᬨ', 'ꦧ': 'ᬩ', 'ꦨ': 'ᬪ', 'ꦩ': 'ᬫ', 'ꦮ': 'ᬯ', 

    'ꦐ': 'ᭅ', 'ꦾ': '᭄ᬬ', 'ꦿ': '᭄ᬭ',
    
    #swara
    'ꦄ': 'ᬅ', 'ꦄꦴ': 'ᬆ', 'ꦅ': 'ᬇ', 'ꦆ': 'ᬈ', 'ꦇ': 'ᬈ', 'ꦎ': 'ᬉ', 'ꦈꦴ': 'ᬊ', 'ꦌ': 'ᬏ', 'ꦍ': 'ᬐ', 'ꦈ': 'ᬑ', 'ꦈꦴ': 'ᬒ', 
    
    
    'ꦉ': 'ᬋ', 'ꦉꦴ': 'ᬌ', 'ꦊ': 'ᬍ', 'ꦋ': 'ᬎ',
    'ꦽ': 'ᬺ', 'ꦽꦴ': 'ᬻ', '꧀ꦭꦼ': 'ᬼ', '꧀ꦭꦼꦴ': 'ᬽ' , '꧀ꦊ': 'ᬼ', '꧀ꦋ': 'ᬽ',

    #sandhangan
    'ꦴ': 'ᬵ', 'ꦶ': 'ᬶ', 'ꦷ': 'ᬷ', 'ꦸ': 'ᬸ', 'ꦹ': 'ᬹ', 'ꦼ': 'ᭂ', 'ꦼꦴ': 'ᭃ', 'ꦺ': 'ᬾ', 'ꦻ': 'ᬿ', 'ꦺꦴ': 'ᭀ', 'ꦻꦴ': 'ᭁ', 
    
    #sigeg
    'ꦀ': 'ᬁ', 'ꦁ': 'ᬂ', 'ꦂ': 'ᬃ', 'ꦃ': 'ᬄ', '꦳': '᬴', '꧀': '᭄',
    
    #Angka
    '꧑': '᭑', '꧒': '᭒', '꧓': '᭓', '꧔': '᭔', '꧕': '᭕', '꧖': '᭖', '꧗': '᭗', '꧘': '᭘', '꧙': '᭙', '꧐': '᭐', 

    #Simbol
    '꧆': '᭜', '꧇': '᭝', '꧈': '᭞', '꧉': '᭟', '꧊': '᭚', '꧅': '᭾', '꧄': '᭛', '꧃': '᭛', '꧋': '᭽', '꧁': '᭛᭜᭛', '꧂': '᭛᭜᭛', 
}

def konversi_aksara_ke_bali(text, daftar_konversi):
    hasil = []
    for karakter in text:
        hasil.append(daftar_konversi.get(karakter, karakter))  # Gunakan karakter asli jika tidak ditemukan
    return ''.join(hasil)

def process_file(input_file, output_file, daftar_konversi):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()
    text = re.sub(r'\u200D', '', text)
    text_terkonversi = konversi_aksara_ke_bali(text, daftar_konversi)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(text_terkonversi)

    print(f"Konversi selesai! Hasil telah disimpan di: {output_file}")

if __name__ == '__main__':
    # Nama file input dan output
    input_file = 'output/output_jawa.txt'  
    output_file = 'output/output_bali.txt' 

    # Memproses file
    process_file(input_file, output_file, daftar_konversi)