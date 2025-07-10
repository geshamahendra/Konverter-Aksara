import re
import sys
import os

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# Daftar konversi aksara Jawa ke Kawi
# Disatukan di sini agar dapat diakses secara global oleh fungsi konversi_aksara_ke_kawi
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
}

sandhangan = {
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

# Gabungkan semua kategori menjadi satu dictionary daftar_konversi global
daftar_konversi = {}
daftar_konversi.update(nglegena)
daftar_konversi.update(swara)
daftar_konversi.update(sandhangan)
daftar_konversi.update(sigeg)
daftar_konversi.update(angka)
daftar_konversi.update(simbol)

# Variabel yang digunakan dalam fungsi tarung
aksara_tarung_panjang = '𑼦𑼖𑼭𑼜𑼨'
joiner = '𑽂'
tarung_panjang_char = '𑼵'
aksara_nglegena = ''.join(nglegena.values())
taling_pepet = ('𑼾', '𑼿', '𑽀')

def tarung(text):
    """
    Mengubah tarung pendek menjadi tarung panjang berdasarkan aturan aksara Kawi.
    """
    taling_group = '|'.join(re.escape(c) for c in taling_pepet) # Escaping for regex
    regex = rf'''
        (                           # Grup 1: Bagian sebelum tarung pendek
            [{re.escape(aksara_tarung_panjang)}]       # Aksara tarung panjang
            (?:{re.escape(joiner)}[{re.escape(aksara_nglegena)}])* # Kombinasi joiner + nglegena (bisa berulang)
            (?:{taling_group})?             # Opsional: salah satu taling
        )
        𑼴                            # Tarung pendek yang akan diubah (escaped)
    '''
    text = re.sub(
        regex,
        lambda m: f"{m.group(1)}{tarung_panjang_char}",
        text,
        flags=re.VERBOSE | re.IGNORECASE # Memungkinkan regex multiline dan case-insensitive
    )
    return text

def retain_final_pangkon(text):
    """
    Memastikan pangkon (sigeg) dipertahankan di akhir baris atau sebelum simbol khusus.
    """
    # Tambahkan simbol khusus yang perlu diperhatikan di akhir
    special_symbols = '𑽅𑽆𑽉𑽌𑽋𑽃𑽍𑽄𑽏𑽇।॥𑽊' # Pastikan karakter di-escape jika perlu
    pattern = rf'{re.escape(joiner)}(?=$|[{re.escape(special_symbols)}])'
    
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Ganti joiner dengan pangkon sesuai aturan
        lines[i] = re.sub(pattern, '𑽁', line)
    
    return "\n".join(lines)

def konversi_aksara_ke_kawi(text):
    """
    Mengkonversi teks yang mengandung aksara Jawa ke aksara Kawi.
    
    Args:
        text (str): Teks input yang akan dikonversi.
        
    Returns:
        str: Teks yang sudah dikonversi ke aksara Kawi.
    """
    # Aturan penggantian khusus sebelum konversi karakter per karakter
    text = re.sub(r'(?<=\b)ꦪꦾꦂ', '𑼂𑼫𑽂𑼫', text, flags=re.IGNORECASE)
    text = re.sub(r'ꦉ\u200Cꦴ', '𑼋', text, flags=re.IGNORECASE)
    text = re.sub(r'ꦫꦾ', '𑼬𑽂𑼫\u200D', text, flags=re.IGNORECASE)
    text = re.sub(r'ꦫ꧀ꦮ', '𑼬𑽂𑼮\u200D', text, flags=re.IGNORECASE)

    hasil = []
    # Lakukan konversi karakter per karakter menggunakan daftar_konversi global
    for karakter in text:
        hasil.append(daftar_konversi.get(karakter, karakter))  # Gunakan karakter asli jika tidak ditemukan
   
    text_hasil = ''.join(hasil)

    # Terapkan aturan tarung panjang
    text_hasil = tarung(text_hasil)
    text_hasil = retain_final_pangkon(text_hasil)  # Memastikan pangkon diproses setelah penggantian
    
    # Penanganan Zero Width Non-Joiner (ZWNJ) dan Zero Width Joiner (ZWJ)
    text_hasil = re.sub(r'𑽂\u200D', '𑽁\u200D', text_hasil)
    text_hasil = re.sub(r'𑽂\u200C', '𑽁\u200C', text_hasil)
    text_hasil = re.sub(r'𑼫𑽂𑼫𑼂\u200D', '𑼂𑼫𑽂𑼫', text_hasil, flags=re.IGNORECASE)
    text_hasil = re.sub(r'𑼂[\u200C\u200D]', '𑼂', text_hasil, flags=re.IGNORECASE)
    
    return text_hasil

def process_file(input_file, output_file):
    """
    Membaca teks dari file input, mengkonversinya ke aksara Kawi,
    dan menulis hasilnya ke file output.
    
    Args:
        input_file (str): Path ke file input.
        output_file (str): Path ke file output.
    """
    # Membaca isi file input
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    # Panggil fungsi konversi_aksara_ke_kawi hanya dengan parameter text
    teks_terkonversi = konversi_aksara_ke_kawi(text)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(teks_terkonversi)

    print(f"Konversi selesai! Hasil telah disimpan di: {output_file}")

if __name__ == '__main__':
    # Nama file input dan output
    input_file = 'output/output_jawa.txt'  
    output_file = 'output/output_kawi.txt'  

    # Memproses file
    process_file(input_file, output_file)
