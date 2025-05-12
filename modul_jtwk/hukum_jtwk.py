import re
from modul_jtwk.kamus_jtwk import substitutions

# Daftar vokal, konsonan, dan simbol yang digunakan untuk regex
daftar_vokal = 'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'è', 'é', 'o', 'ō', 'ö', 'ŏ', 'ĕ', 'ꜷ', 'ꜽ', 'â', 'î', 'ê', 'û', 'ô'
vokal_regex = ''.join(daftar_vokal)
daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
semi_vokal = 'lwyr'
daftar_tidak_digandakan = {
    'n', 'ṅ', 'ṇ', 'h', 'ṣ', 's', 'c', 'ꞓ', 'r', 'ṙ', 'ṫ', 'ŧ', 'ꝑ', 'ǥ', 'ɉ', 'ƀ', 'ꝁ', 'k', 'ḍ', 'ḋ', 'd', 'đ',
}
zwnj = "\u200C"
# Fungsi untuk menambahkan ZWNJ di awal kata
def add_zwnj_awal_kata(text, pattern, replacement):
    def replacer(m):
        start = m.start()
        if start == 0 or text[start - 1] == '\n':
            return m.group(0)  # Jangan ubah kalau di awal baris
        return replacement + m.group(0)
    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)

# Fungsi untuk memperbaiki kata baku
def kata_baku(text):
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
    #'rĕ': 'ṛĕ',
    #'rö': 'ṝö',
    'ṣt': 'ṣṭ',
    'sṭ': 'ṣṭ',
    'ṣŧ': 'ṣṫ',
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
    #kasus " ṅ h..."
    text = re.sub(r'\s+ŋ\s+h', ' ṅ h', text, flags=re.IGNORECASE)

    #tambah zwnj depan kata
    for pattern in [r'\bww', r'\byw', r'wru', r'\brw', r'lwir' , r'\byan\b', r'\btan\b', r'\bṅw', r'\bmw', r'\bstr', r'\brkw', r'\b(riṅ|ring|riŋ|ri)', r'\bdwa\b', r'\bya\b', r'\bta(?:n|ṅ|ŋ)?\b']:#, r'\bry\b' #r'\blwir'
        text = add_zwnj_awal_kata(text, pattern, '\u200C')
    
    #khusus duhka
    text = re.sub(r'(duhk|duhꝁ)([' + vokal_regex + '])',lambda m: ('duḥk' if m.group(1) == 'duhk' else 'duḥꝁ') + m.group(2), text)
    
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
        r'res': 'ṛĕṣ',
        r'rĕs': 'ṛĕṣ',
        r'ṙṣik\b': 'ṙsik',
        r'ṙṇny': 'ṙny',
        r'aṙyya\b': 'arya',
        r'ṙyyakĕn\b': 'ryakĕn',
        r'ṙmmu ': 'ṙmu ',
        r'[^\S\n]+lĕ': ' ‌lĕ',     #zwnj lĕ untuk mencegah lĕ
        r'r\u200c': 'ṙ', #r+zwnj agar tidak menjadi ra pangku
        r'ṙ\u200c': 'ṙ'
    }

    # Terapkan semua penggantian spesial
    for pola, ganti in penggantian_spesial.items():
        text = re.sub(pola, ganti, text)

    VOWEL_PENDEK = 'aiuĕAIUĔ'
    # regex substitution
    #text = re.sub(r'(?<=[%s])ṙ([%s])\1' % (VOWEL_PENDEK, daftar_konsonan), r'r\1', text)

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
    #ubah ṙ jadi r diujung baris
    text = re.sub(r'ṙ[ \t]*\n', 'r\n', text)
    text = re.sub(r'ry\s+\u200c', r'ry ', text)
    # Ubah vokal kapital jadi kecil jika didahului spasi (bukan \n) atau tanda -
    text = re.sub(r'(?<=[ \t\r\f\v\-])([AEIOU])', lambda m: m.group(1).lower(), text)
    
    return(text)
