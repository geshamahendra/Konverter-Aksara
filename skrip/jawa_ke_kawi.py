import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

nglegena = {
    'ꦏ': '𑼒', 'ꦑ': '𑼓', 'ꦒ': '𑼔', 'ꦓ': '𑼕', 'ꦔ': '𑼖', 'ꦲ': '𑼲',
    'ꦕ': '𑼗', 'ꦖ': '𑼘', 'ꦗ': '𑼙', 'ꦘ': '𑼳', 'ꦙ': '𑼚', 'ꦚ': '𑼛', 'ꦯ': '𑼯', 'ꦪ': '𑼫', 
    'ꦛ': '𑼜', 'ꦜ': '𑼝', 'ꦝ': '𑼞', 'ꦞ': '𑼟', 'ꦟ': '𑼠', 'ꦰ': '𑼰', 'ꦫ': '𑼬', 
    'ꦠ': '𑼡', 'ꦡ': '𑼢', 'ꦢ': '𑼣', 'ꦣ': '𑼤', 'ꦤ': '𑼥', 'ꦱ': '𑼱', 'ꦭ': '𑼭',
    'ꦥ': '𑼦', 'ꦦ': '𑼧', 'ꦧ': '𑼨', 'ꦨ': '𑼩', 'ꦩ': '𑼪', 'ꦮ': '𑼮', 

    'ꦾ': '𑽂𑼫', 'ꦿ': '𑽂𑼬',
}

swara = {
    'ꦄ': '𑼄', 'ꦄꦴ': '𑼅', 'ꦅ': '𑼆', 'ꦆ': '𑼇', 'ꦇ': '𑼇', 'ꦎ': '𑼈', 'ꦎꦴ': '𑼉', 'ꦌ': '𑼎', 'ꦍ': '𑼏', 'ꦈ': '𑼐', 'ꦈꦴ': '𑼐𑼴', 
    

    'ꦉ': '𑼊', 'ꦉꦴ': '𑼋', 'ꦊ': '𑼌', 'ꦋ': '𑼍',
    'ꦽ': '𑼺', 'ꦽꦴ': '𑼺𑼴', 
    #'꧀ꦭꦼ': 'ᬼ', '꧀ꦭꦼꦴ': 'ᬽ', '꧀ꦊ': 'ᬼ', '꧀ꦋ': 'ᬽ',


}

sandhangan = {
    #'ꦴ': '𑼵', 'ꦺꦴ': '𑼾𑼵', 'ꦻꦴ': '𑼿𑼵', 'ꦼꦴ': '𑽀𑼴',
    'ꦴ': '𑼴', 'ꦺꦴ': '𑼾𑼴', 'ꦻꦴ': '𑼿𑼴',
    'ꦶ': '𑼶', 'ꦷ': '𑼷', 'ꦸ': '𑼸', 'ꦹ': '𑼹', 'ꦼ': '𑽀', 'ꦺ': '𑼾', 'ꦻ': '𑼿',   

}
sigeg = {
    'ꦀ': '𑼀', 'ꦁ': '𑼁', 'ꦂ': '𑼂', 'ꦃ': '𑼃', '꦳': '꦳', '꧀': '𑽂',
}

angka = {
    '꧑': '𑽑', '꧒': '𑽒', '꧓': '𑽓', '꧔': '𑽔', '꧕': '𑽕', '꧖': '𑽖', '꧗': '𑽗', '꧘': '𑽘', '꧙': '𑽙', '꧐': '𑽐', 
}

simbol = {
    '꧆': '𑽌', '꧇': '𑽋', '꧈': '𑽉', '꧉': '𑽊', '꧊': '𑽃', '꧅': '𑽆', '꧄': '𑽅', '꧃': '𑽍', '꧋': '𑽄', 
    '_': '𑽏', '꧁': '𑽇', '꧂': '𑽇', 
}

# Gabungkan semua kategori menjadi satu dictionary
daftar_konversi = {}
daftar_konversi.update(nglegena)
daftar_konversi.update(swara)
daftar_konversi.update(sandhangan)
daftar_konversi.update(sigeg)
daftar_konversi.update(angka)
daftar_konversi.update(simbol)

# Daftar aksara dengan tarung panjang
aksara_tarung_panjang = '𑼦𑼖𑼭𑼜𑼨'
joiner = '𑽂'
tarung_panjang_char = '𑼵'
aksara_nglegena = ''.join(nglegena.values())
taling_1 = '𑼾'
taling_2 = '𑼿'
taling_pepet = ('𑼾', '𑼿', '𑽀')

def tarung(text):
    # Gabungkan semua pola ke dalam satu regex
    taling_group = '|'.join(taling_pepet)  # Membuat grup untuk taling
    regex = rf'''
        (                           # Grup 1: Bagian sebelum tarung pendek
            [{aksara_tarung_panjang}]       # Aksara tarung panjang
            (?:{joiner}[{aksara_nglegena}])*  # Kombinasi joiner + nglegena (bisa berulang)
            (?:{taling_group})?             # Opsional: salah satu taling
        )
        𑼴                            # Tarung pendek yang akan diubah
    '''
    # Terapkan regex
    text = re.sub(
        regex,
        lambda m: f"{m.group(1)}{tarung_panjang_char}",
        text,
        flags=re.VERBOSE  # Memungkinkan regex multiline untuk keterbacaan
    )
    return text

def konversi_aksara_ke_kawi(text, daftar_konversi):
    hasil = []
    for karakter in text:
        hasil.append(daftar_konversi.get(karakter, karakter))  # Gunakan karakter asli jika tidak ditemukan
   
    text = ''.join(hasil)

    # Terapkan aturan tarung panjang
    text = tarung(text)
    text = retain_final_pangkon(text)  # Memastikan pangkon diproses setelah penggantian
    
    #zwnj
    text = re.sub(r'𑽂\u200C', '𑽁\u200C', text)
    return text


def retain_final_pangkon(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Additionally replace 'ṙ' with 'r' at the end of the line if followed by non-letter characters or nothing
        lines[i] = re.sub(r'𑽂(?=\W*$)', '𑽁', line)
    # Rejoin the lines into a single text block
    return "\n".join(lines)

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
    output_file = 'output/output_kawi.txt'  

    # Memproses file
    process_file(input_file, output_file, daftar_konversi)