import re
from modul_jtwk.kamus_jtwk import substitutions

# Daftar vokal, konsonan, dan simbol yang digunakan untuk regex
daftar_vokal = 'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'è', 'o', 'ō', 'ö', 'ŏ', 'ĕ', 'ꜷ', 'ꜽ', 'â', 'î', 'ê', 'û', 'ô'
vokal_regex = ''.join(daftar_vokal)
daftar_konsonan = "bcdfghjklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
semi_vokal = 'lwyr'
daftar_tidak_digandakan = {
    'n', 'ṅ', 'ṇ', 'h', 'ṣ', 's', 'c', 'ꞓ', 'r', 'ṙ', 'ṫ', 'ŧ', 'ꝑ', 'ǥ', 'ɉ', 'ƀ', 'ꝁ', 'k', 'ḍ', 'ḋ', 'd', 'đ',
}
    
# Fungsi untuk menghitung simbol metrum
def process_baris(baris):
    # Jangan proses kalau tidak ada simbol metrum
    if not re.search(r'[–⏑⏓]', baris):
        return baris

    # Jika ada tanda [ ] maka lakukan perhitungan khusus
    if "[" in baris and "]" in baris:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', baris)

        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))

            # Bersihkan spasi dan karakter tak terlihat
            isi_bersih = re.sub(r'[\u200C\u200D\s]', '', isi)

            # Hitung jumlah nada dalam blok, termasuk tanda -
            jumlah_dalam_blok = len(re.findall(r'[–⏑⏓-]', isi_bersih))

            # Hitung jumlah di luar blok
            baris_di_luar = baris[:match.start()] + baris[match.end():]
            jumlah_di_luar = len(re.findall(r'[–⏑⏓]', baris_di_luar))

            jumlah_total = (jumlah_dalam_blok * perkalian) + jumlah_di_luar
        else:
            jumlah_total = len(re.findall(r'[–⏑⏓]', baris))
    else:
        # Tidak ada blok [], pakai metode biasa
        jumlah_total = len(re.findall(r'[–⏑⏓]', baris))

    return baris.rstrip() + f" : {jumlah_total}"

# Fungsi untuk menambahkan ZWNJ di awal kata
def add_zwnj_awal_kata(text, pattern, replacement):
    def replacer(m):
        start = m.start()
        if start == 0 or text[start - 1] == '\n':
            return m.group(0)  # Jangan ubah kalau di awal baris
        return replacement + m.group(0)
    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)

def ubah_ry_ri_awal_kata(teks):
    hasil = []
    ubah = False
    baris_metrum_berikutnya = False

    baris_list = teks.splitlines()
    i = 0
    while i < len(baris_list):
        baris = baris_list[i]

        if baris.startswith('<'):
            # Cek baris berikutnya apakah metrum dengan ⏑ di awal
            if i + 1 < len(baris_list) and baris_list[i + 1].strip().startswith('⏑'):
                ubah = False
            else:
                ubah = True
        elif baris.strip().startswith('–'):
            ubah = True
        elif baris.strip().startswith('<'):
            ubah = False

        if ubah:
            # Ganti "ry"/"ri" di awal kata (case insensitive)
            def ganti_awalan(match):
                huruf_pertama = match.group(1)
                return huruf_pertama + 'ī'
            baris = re.sub(r'\b([Rr])[YyIi]', ganti_awalan, baris)

        hasil.append(baris)
        i += 1

    return "\n".join(hasil)

# Fungsi untuk memperbaiki kata baku
def kata_baku(text):
    #text = ubah_ry_ri_awal_kata(text)
    #text = proses_ry_metrum(text)
    
    # Menyesuaikan huruf vokal pada awal kata
    text = re.sub(rf'(^|\n)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)
    #text = text.replace("\n", "\u200C\n")

    for pattern, replacement in substitutions.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    text = re.sub(r'([yw])\b[^\S\n]+([AEIOUĀĪŪĒŌÖŎĔꜶꜸ])', lambda m: m.group(1) + ' ' + m.group(2).lower(), text)

    return(text)

# Fungsi untuk mengubah hukum aksara
def hukum_aksara(text):

    text = re.sub(r'(?<=\w)sṭ(?:h)?(?=\w)', lambda m: 'ṣṫ' if m.group(0).endswith('h') else 'ṣṭ', text)
    text = re.sub(r'sṭ', 'ṣṭ', text, flags=re.IGNORECASE)
    text = re.sub(r'sṫ', 'ṣṫ', text, flags=re.IGNORECASE)
    text = re.sub(r'sry', 'śry', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAi\b', 'Ꜽ', text)
    text = re.sub(r'\bAu\b', 'Ꜷ', text)
    text = re.sub(r'\b^h', 'ʰ', text)
    
    replacements = {
    'nḍ': 'ṇḍ',
    'nḋ': 'ṇḋ',
    'nṭ': 'ṇṭ',
    'nṫ': 'ṇṫ',
    'nc': 'ñc',
    'nj': 'ñj',
    'ks': 'kṣ',
    'ꝁs': 'ꝁṣ',
    'gs': 'gṣ',
    'ǥs': 'ǥṣ',
    # 'ṅs': 'ṅṣ',
    'jn': 'jñ',
    'rs': 'ṙṣ',
    'rĕ': 'ṛĕ',
    'rö': 'ṝö',
    'ṣt': 'ṣṭ',
    'sṭ': 'ṣṭ',
    'ṣŧ': 'ṣṫ',
    'sŧ': 'ṣṫ',
}

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return(text)

# Fungsi untuk mengatur hukum sigeg
def hukum_sigeg(text):
    text = re.sub(r'ṅ\b', 'ŋ', text)
    text = re.sub(r'h(?!\w)', 'ḥ', text, flags=re.IGNORECASE)  
    text = re.sub(r'ng(?=\w)', 'ṅ', text, flags=re.IGNORECASE)  
    text = re.sub(r'ng(?!\w)', 'ŋ', text, flags=re.IGNORECASE)
    
    return(text)

# Fungsi untuk mengubah hukum ṙ
def hukum_ṙ(text):
    # Bersihkan konsonan yang digandakan setelah ṙ
    #text = re.sub(rf'(?<=[ṙ])([{daftar_konsonan}])\1+', lambda m: m.group(0) if m.group(1) in daftar_tidak_digandakan else m.group(1), text)
    # Ubah ṙ + konsonan ganda menjadi r + satu konsonan saja (misalnya ṙjj → rj)
    text = re.sub(r'r([' + daftar_konsonan + r'])\1', r'r\1', text)

    # Step tambahan untuk menangani kluster seperti "gra", "kra", "dra", dll
    text = re.sub(rf'(?<=\w)r(?=([{daftar_konsonan}])([{semi_vokal}]))', 'ṙ', text)

    # 1. Ubah 'r' menjadi 'ṙ' jika setelahnya konsonan + vokal
    text = re.sub(rf'(?<=\w)r(?=([{daftar_konsonan}])[{vokal_regex}])', 'ṙ', text)

    #2. gandakan huruf konsonan setelah ṙ, kecuali yang dalam daftar_tidak_digandakan
    text = re.sub(rf'(?<=ṙ)([{daftar_konsonan}])', lambda m: m.group(1) if m.group(1) in daftar_tidak_digandakan else m.group(1) * 2, text)
    # 3. ROLLBACK: Jika sebelum ṙ ada konsonan
    def rollback_if_preceded_by_consonant(match):
        prev = match.group(1)
        kons = match.group(2)
        return f'{prev}r{kons}'

    text = re.sub(rf'([{daftar_konsonan}])ṙ([{daftar_konsonan}])\2?', rollback_if_preceded_by_consonant, text)
    # ubah kembali ṙ ke r jika setelahnya justru vokal
    text = re.sub(rf'(?<=ṙ)(?=[{vokal_regex}])', 'r', text)

    # Mahaprana
    mahaprana = {
        'ṙk': 'ṙkk',
        'ṙꝁ': 'ṙkꝁ',
        'ṙṫ': 'ṙṭṫ',
        'ṙꝑ': 'ṙpꝑ',
        'ṙǥ': 'ṙgǥ',
        'ṙɉ': 'ṙjɉ',
        'ṙƀ': 'ṙbƀ',
        'ṙs': 'ṙṣ',
        'ṛs': 'ṛṣ',
        'res': 'ṛĕṣ',
        'rĕs': 'ṛĕṣ',
        'ṙṇ': 'ṙṇṇ',
        'ṙn': 'ṙṇn',
        'ṙd': 'ṙdd',
        'ṙđ': 'ṙdđ',
        'ṙḍ': 'ṙdḍ',
        'ṙḋ': 'ṙdḋ',
        'ṙc': 'ṙcc',
        'ṙꞓ': 'ṙcꞓ'
    }
    for pattern, replacement in mahaprana.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    #kasus ry ṙyy
    #text = re.sub(r'(?:(?<=^)|(?<=\s))ry(?=\S)', '\u200cṙyy', text, flags=re.MULTILINE)
    #text = re.sub(r'(rī\b[^\S\n]+a|[^\S\n]+ṙyy)', '\u200cṙyy', text, flags=re.IGNORECASE)
    text = re.sub(
    r'(?:(?<=^)|(?<=\s))ry(?=\S)|(?:rī\b[^\S\n]+a|[^\S\n]+ṙyy)', '\u200cṙyy', text, flags=re.MULTILINE | re.IGNORECASE)

    return(text)

# Fungsi untuk finalisasi (penyesuaian akhir)
def finalisasi(text):
    for pattern in [r'\bww', r'\byw', r'wru', r'\brw', r'lwir' , r'\byan\b', r'\btan\b', r'\bṅw', r'\bmw', r'\bstr', r'\brkw', r'\b(riṅ|ring|riŋ|ri)', r'\bdwa\b']:#, r'\bry\b' #r'\blwir'
        text = add_zwnj_awal_kata(text, pattern, '\u200C')

    #mempertahankan le
    text = re.sub(r'(?<=[bcdfghjklmnpqrstvwxyzḍḋḷṅṇñṇśṣṭṯṙṝꝁǥꞓƀǥɉƀ])(lĕ|ḷĕ|ḷ)', lambda m: m.group(1) + '\u200D', text, flags=re.IGNORECASE)

    #kasus spesial pasanyan nya
    for huruf, ganti in [('r', 'ṙ'), ('h', 'ḥ'), ('ṅ', 'ŋ')]:
        text = re.sub(rf'{huruf}(?=nṇ?y[{vokal_regex}])', ganti, text, flags=re.IGNORECASE)
    #spesial kata r nya
    text = re.sub(r'ṙṇny', 'ṙny', text)

    # Proses dan gabungkan hasil per baris pada teks
    text = "\n".join(process_baris(baris) for baris in text.splitlines())

    
    #spesial kata arsik
    text = re.sub(r'ṙṣik\b', 'ṙsik', text)
    
    #zwnj ṅ ḥ
    text = re.sub(r'[ṅh]\u200c', lambda m: 'ŋ' if m.group(0) == 'ṅ\u200c' else 'ḥ', text)
    
    # ganti 'r' jadi ṙ jika diikuti spasi atau tanda hubung
    text = re.sub(r'(?<=\w)r(?=[\s-])', 'ṙ', text)
    text = re.sub(r'ṙ[ \t]*\n', 'r\n', text)


    return(text)
