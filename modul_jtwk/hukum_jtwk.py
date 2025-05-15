import re
from modul_jtwk.kamus_jtwk import substitutions

# Daftar vokal, konsonan, dan simbol yang digunakan untuk regex
daftar_vokal = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'è', 'é', 'o', 'ō', 'ö', 'ŏ', 'ĕ', 'ꜷ', 'ꜽ', 'â', 'î', 'ê', 'û', 'ô']
vokal_regex = "(" + "|".join(daftar_vokal) + ")"
daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
semi_vokal = 'lwyr'
daftar_tidak_digandakan = {
    'n', 'ṅ', 'ṇ', 'h', 'ṣ', 's', 'c', 'ꞓ', 'r', 'ṙ', 'ṫ', 'ŧ', 'ꝑ', 'ǥ', 'ɉ', 'ƀ', 'ꝁ', 'k', 'ḍ', 'ḋ', 'd', 'đ',
}
vokal_pendek = 'aiuĕAIUĔ'

zwnj = "\u200C"
# Fungsi untuk menambahkan ZWNJ di awal kata jika didepannya konsonan
def add_zwnj_awal_kata_bulk(text, patterns, replacement, daftar_konsonan):
    def is_prev_char_konsonan(text, pos):
        # Lewati spasi/tab/newline ke belakang hingga ketemu huruf bukan spasi
        i = pos - 1
        while i >= 0 and text[i] in ' \t\r\n':
            i -= 1
        return i >= 0 and text[i] in daftar_konsonan

    combined_pattern = '|'.join(f'(?:{p})' for p in patterns)
    regex = re.compile(combined_pattern, flags=re.IGNORECASE)

    result = []
    last_idx = 0

    for m in regex.finditer(text):
        start = m.start()
        result.append(text[last_idx:start])

        if start == 0 or text[start - 1] == '\n':
            result.append(m.group(0))
        elif is_prev_char_konsonan(text, start):
            result.append(replacement + m.group(0))
        else:
            result.append(m.group(0))

        last_idx = m.end()

    result.append(text[last_idx:])
    return ''.join(result)

# Fungsi untuk memperbaiki kata baku
def kata_baku(text):
    # Menyesuaikan huruf vokal pada awal kata
    text = re.sub(rf'(^|\n)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)
    #text = text.replace("\n", "\u200C\n")

    for pattern, replacement in substitutions.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    text = re.sub(r'([yw])\b[^\S\n]+([AEIOUĀĪŪĒŌÖŎĔꜶꜸ])', lambda m: m.group(1) + ' ' + m.group(2).lower(), text)

    return(text)

#Fungsi untuk mengubah kapital
mapping_vokal = {
    'A': 'a',
    'Ā': 'ā',
    'Â': 'â',
    'I': 'i',
    'Ī': 'ī',
    'Î': 'î',
    'U': 'u',
    'Ū': 'ū',
    'Û': 'û',
    'O': 'o',
    'Ō': 'ō',
    'Ô': 'ô',
    'E': 'e',
    'Ê': 'ê',
    'É': 'é',
    'È': 'è',
    'Ꜽ': 'ꜽ',
    'Ꜷ': 'ꜷ'
    }
def lower_capital_vowels(match):
    capital_vowel = match.group(1)
    return mapping_vokal.get(capital_vowel, capital_vowel.lower()) # Menggunakan .lower() sebagai fallback

#hukum aksara suci
def replace_vokal_m(match):
    vokal_kecil = match.group(1)
    mm = match.group(2)
    vokal_kapital = vokal_kecil.upper()
    return f"\u200C{vokal_kapital}{mm}\u200C"

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
    'jn': 'jñ',
    'rs': 'ṙṣ',
    'ṣt': 'ṣṭ',
    'sṭ': 'ṣṭ',
    'ṣŧ': 'ṣṫ',
}

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return(text)

# Fungsi untuk mengatur hukum sigeg
def hukum_sigeg(text):
    text = re.sub(r'ng', 'ṅ', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<!^)(?<!\n)ṅ\b', 'ŋ', text)
    text = re.sub(r'(?<!^)(?<!\n)h\b', 'ḥ', text)    
    
    #kasus " ṅ h..."
    text = re.sub(r'\s+ŋ\s+h', ' ṅh', text, flags=re.IGNORECASE)

    #kasus ŋ berdiri di depan konsonan
    text = re.sub(r"(" + f"[{daftar_konsonan}]" + r")\s*(ŋ)\s+(" + f"[{daftar_konsonan}]" + r")", r"\1 ṅ-\3", text, flags=re.IGNORECASE)

    #kasus ṅ berulang
    #text = re.sub(r'(\w)(\w)ṅ-(\1\2)ŋ', r'\1\2ŋ\1\2ŋ', text)

    #tambah zwnj depan kata
    patterns = [
    r'\bww', r'\byw', r'wr', r'\brw', r'lwi(r|ṙ)', r'\byan\b', r'\btan\b',
    r"\bṅ(-)?(" + f"[{daftar_konsonan}]" + r")", r'\bmw', r'\bstr', r'\brkw', r'\b(riṅ|ring|riŋ|ri)',
    r'\bdwa\b', r'\bya\b', r'[' + daftar_konsonan + r']ta(?:n|ṅ|ŋ)?\b']
    text = add_zwnj_awal_kata_bulk(text, patterns, '\u200C', daftar_konsonan) 
    
    #khusus duhka
    text = re.sub(r'(duhk|duhꝁ)([' + vokal_regex + '])',lambda m: ('duḥk' if m.group(1) == 'duhk' else 'duḥꝁ') + m.group(2), text)
    
    return(text)

# Fungsi untuk mengubah hukum ṙ
def hukum_ṙ(text):
    # Bersihkan konsonan yang digandakan setelah ṙ/r (misalnya ṙjj → rj)
    text = re.sub(r'[rṙ]([' + daftar_konsonan + r'])\1', r'r\1', text)

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
    text = re.sub(
    r'(?:(?<=^)|(?<=\s))ry(?=\S)|(?:rī\b[^\S\n]+a|[^\S\n]+ṙyy)', '\u200cṙyy', text, flags=re.MULTILINE | re.IGNORECASE)
    # ganti 'r' jadi ṙ jika diikuti spasi atau tanda hubung
    text = re.sub(r'(?<=\w)r(?=[\s-])', 'ṙ', text)

    # Daftar penggantian spesial
    penggantian_spesial = {
        r'ṙs': 'ṙṣ',
        r'ṛs': 'ṛṣ',
        #r'res': 'ṛĕṣ',
        #r'rĕs': 'ṛĕṣ',
        r'ṙṣik\b': 'ṙsik',
        r'ṙṇny': 'ṙny',
        r'aṙyy(a|ā)': r'ary\1',
        r'āścary' : r'āścaṙyy',
        r'ṙyyakĕn\b': 'ryakĕn',
        r'uṙww': 'urw',
        r'ṙmmu ': 'ṙmu ',
        r'[^\S\n]+lĕ': ' ‌lĕ',     #zwnj lĕ untuk mencegah lĕ
        r'r\u200c': 'ṙ', #r+zwnj agar tidak menjadi ra pangku
        r'ṙ\u200c': 'ṙ',
        r'^ŋ':r'ṅ'
        #r'([' + vokal_regex + r'])m\b': r'\1m\u200c'
    }

    # Terapkan semua penggantian spesial
    for pola, ganti in penggantian_spesial.items():
        text = re.sub(pola, ganti, text)

    return(text)

# Fungsi untuk finalisasi (penyesuaian akhir)
def finalisasi(text):

    #mempertahankan le
    text = re.sub(r'(?<=[bcdfghjklmnpqrstvwxyzḍḋḷṅṇñṇśṣṭṯṙṝꝁǥꞓƀǥɉƀ])(lĕ|ḷĕ|ḷ)', lambda m: m.group(1) + '\u200D', text, flags=re.IGNORECASE)

    #kasus spesial pasanyan nya
    for huruf, ganti in [('r', 'ṙ'), ('h', 'ḥ'), ('ṅ', 'ŋ')]:
        text = re.sub(rf'{huruf}(?=nṇ?y[{vokal_regex}])', ganti, text, flags=re.IGNORECASE)

    #sigeg bertemu sigeg
    text = re.sub(r'ṙ[^\S\n]*ŋ', r'ṙ ṅ', text)
    text = re.sub(r'ḥ[^\S\n]*ŋ', r'ḥ ṅ', text)
    text = re.sub(r'^[^\S\n]*ŋ', r'ṅ', text, re.MULTILINE)
    #ubah ṙ jadi r diujung baris
    text = re.sub(r'ṙ[ \t]*\n', 'r\n', text)
    text = re.sub(r'ry\s+\u200c', r'ry ', text)

    #aksara suci
    text = re.sub(rf' {vokal_regex}(m|ṃ) ', replace_vokal_m, text)

    #=====Modifikasi lebih lanjut tentang huruf vokal====
    daftar_vokal = "aāâiīîuūûeèéêoōöŏôĕꜷꜽ"  # Daftar vokal
    zwnj = '\u200C'  # Zero-width non-joiner (ZWNJ)
    kapitalisasi_khusus = {'ꜽ': 'Ꜽ','è': 'È', 'é': 'É', }
    
    # Kapitalkan vokal di awal baris
    text = re.sub(
    rf'^([{daftar_vokal}])',lambda m: kapitalisasi_khusus.get(m.group(1), m.group(1).upper()),text,flags=re.MULTILINE)
    
    # Menyisipkan ZWNJ dan mengkapitalkan vokal jika didahului tanda baca non-huruf (bukan spasi/strip)
    text = re.sub(rf'([^\w\s-])(\s*)([{daftar_vokal}])',lambda m: f"{m.group(1)}{m.group(2)}{zwnj}{m.group(3).upper()}",text)

    # Ubah vokal kapital jadi kecil jika didahului spasi (bukan \n) atau tanda -
    text = re.sub(r'(?<=[ \t\r\f\v\-])([AĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ])', lower_capital_vowels, text)

    
    return(text)
