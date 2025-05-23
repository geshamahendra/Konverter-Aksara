import re
from modul_jtwk.kamus_jtwk import substitutions

# Daftar vokal, konsonan, dan simbol yang digunakan untuk regex
DAFTAR_VOKAL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûôAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOKAL_REGEX = f"[{DAFTAR_VOKAL}]"
VOKAL_REGEX_GROUPED = f"({VOKAL_REGEX})"
DAFTAR_KONSONAN = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
SEMI_VOKAL = 'lwyr'
TIDAK_DIGANDAKAN = set('nṅṇhṣscꞓrṙṫŧꝑǥɉƀꝁkdḍḋdđ')
VOKAL_PENDEK = 'aiuĕAIUĔ'
AWAL_BARIS = r'(^|\n)'
NON_HURUF_PENDAHULU = r'([^\w\s-])(\s*)'

# Pre-compile regex untuk efisiensi
SUBSTITUTION_REGEX = [(re.compile(pattern), replacement) for pattern, replacement in substitutions.items()]
KAPITAL_KE_KECIL = {
    'A': 'a', 'Ā': 'ā', 'Â': 'â', 'I': 'i', 'Ī': 'ī', 'Î': 'î', 'U': 'u',
    'Ū': 'ū', 'Û': 'û', 'O': 'o', 'Ō': 'ō', 'Ô': 'ô', 'E': 'e', 'Ê': 'ê',
    'É': 'é', 'È': 'è', 'Ꜽ': 'ꜽ', 'Ꜷ': 'ꜷ'
}
HUKUM_AKSARA_REPLACEMENTS = {
    r'nḍ': 'ṇḍ', r'nḋ': 'ṇḋ', r'nṭ': 'ṇṭ', r'nṫ': 'ṇṫ', r'nc': 'ñc',
    r'nj': 'ñj', r'ks': 'kṣ', r'ꝁs': 'ꝁṣ', r'gs': 'gṣ', r'ǥs': 'ǥṣ',
    r'jn': 'jñ', r'rs': 'ṙṣ', r'ṣt': 'ṣṭ', r'sṭ': 'ṣṭ', r'ṣŧ': 'ṣṫ',
    r'(?<=\w)sṭ(?:h)?(?=\w)': lambda m: 'ṣṫ' if m.group(0).endswith('h') else 'ṣṭ',
    r'sry': 'śry', r'sṭ': 'ṣṭ', r'sṫ': 'ṣṫ'
}
HUKUM_ṙ_MAHAPRANA = {
    'ṙk': 'ṙkk', 'ṙꝁ': 'ṙkꝁ', 'ṙṫ': 'ṙṭṫ', 'ṙꝑ': 'ṙpꝑ',
    'ṙǥ': 'ṙgǥ', 'ṙɉ': 'ṙjɉ', 'ṙƀ': 'ṙbƀ', 'ṙṇ': 'ṙṇṇ',
    'ṙn': 'ṙṇn', 'ṙd': 'ṙdd', 'ṙđ': 'ṙdđ', 'ṙḍ': 'ṙdḍ',
    'ṙḋ': 'ṙdḋ', 'ṙc': 'ṙcc', 'ṙꞓ': 'ṙcꞓ'
}
PENGGANTIAN_SPESIAL = {
    #rf'(?<![{DAFTAR_VOKAL}])y\b\s+': 'y-', 
    #rf'(?<![{DAFTAR_VOKAL}])w\b\s+': 'w-',

    r'ṙs': 'ṙṣ', r'ṛs': 'ṛṣ',
    r'ṙṣik\b': 'ṙsik', 
    r'ṙṇny': 'ṙny',

    r'aṙyy([aā])': r'ary\1',
    r'āś([cꞓ])ary': r'āś\1aṙyy', r'ṙyyakĕn\b': 'ryakĕn', r'uṙww': 'urw',
    r'ṙmmu ': 'ṙmu ', 
    r'r\u200c': 'ṙ', r'ṙ\u200c': 'ṙ',
    r'^ŋ': 'ṅ'
}

FINALISASI_PENGGANTI = [
    (re.compile(rf'([rhṅ])(?=nṇ?y{VOKAL_REGEX})'), lambda m: {'r': 'ṙ', 'h': 'ḥ', 'ṅ': 'ŋ'}[m.group(1)]), #kasus spesial pasanyan nya
    (re.compile(r'ṙ[^\S\n]*ŋ'), r'ṙ ṅ'), #sigeg bertemu sigeg
    (re.compile(r'ḥ[^\S\n]*ŋ'), r'ḥ ṅ'), #sigeg bertemu sigeg
    (re.compile(r'^[^\S\n]*ŋ', re.MULTILINE), r'ṅ'), #ubah ṙ jadi r diujung baris
    (re.compile(r'ṙ[ \t]*\n'), r'r\n'), #ubah ṙ jadi r diujung baris
    (re.compile(r'[^\S\n]+'), ' '), #hapus spasi yang terlalu banyak

    (re.compile(rf'^([{DAFTAR_VOKAL}])', re.MULTILINE), lambda m: {'ꜽ': 'Ꜽ', 'è': 'È', 'é': 'É'}.get(m.group(1), m.group(1).upper())), #Kapitalkan vokal di awal baris
    (re.compile(rf'{NON_HURUF_PENDAHULU}({VOKAL_REGEX})'), lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).upper()}"), #Kapitalkan vokal jika didahului tanda baca non-huruf (bukan spasi/strip)
    (re.compile(rf'`({VOKAL_REGEX})'),lambda m: m.group(1).upper()) #kapitalkan vokal jika didepannya ada backtick
]

# Fungsi untuk memperbaiki kata baku
def kata_baku(text):
    # Kapitalkan huruf vokal pada awal baris
    text = re.sub(rf'{AWAL_BARIS}({VOKAL_REGEX})', lambda m: m.group(1) + m.group(2).upper(), text)

    # Terapkan substitusi kamus_jtwk
    for pattern, replacement in SUBSTITUTION_REGEX:
        text = pattern.sub(replacement, text)

    return text


#Fungsi untuk mengubah kapital
def lower_capital_vowels(match):
    capital_vowel = match.group(1)
    return KAPITAL_KE_KECIL.get(capital_vowel, capital_vowel.lower()) # Menggunakan .lower() sebagai fallback

# Fungsi untuk mengubah hukum aksara
def hukum_aksara(text):

    #==============Hukum konsonan=================
    for pattern, replacement in HUKUM_AKSARA_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# Fungsi untuk mengatur hukum sigeg
def hukum_sigeg(text):

    #Kasus konsonan berdiri diantara spasi
    text = re.sub(rf"([{DAFTAR_KONSONAN}])(\s*|-)([{DAFTAR_KONSONAN}])\s+([{DAFTAR_VOKAL}])", r"\1\2\3-\4", text, flags=re.IGNORECASE)

    #kecualikan penyigegan jika setelahnya - dari regex diatas
    text = re.sub(r'(?<!^)(?<!\n)ṅ\b(?!-)', 'ŋ', text)
    text = re.sub(r'(?<!^)(?<!\n)h\b(?!-)', 'ḥ', text)
    #kasus " ṅ h..."
    text = re.sub(r'\s+ŋ\s+h', ' ṅh', text, flags=re.IGNORECASE)

    #kasus ṅ berulang
    #text = re.sub(r'(\w)(\w)ṅ-(\1\2)ŋ', r'\1\2ŋ\1\2ŋ', text)

    return text

# Fungsi untuk mengubah hukum ṙ
def hukum_ṙ(text):
    # Bersihkan konsonan yang digandakan setelah ṙ/r (misalnya ṙjj → rj)
    text = re.sub(r'[rṙ]([' + DAFTAR_KONSONAN + r'])\1', r'r\1', text)
    # Step tambahan untuk menangani kluster seperti "gra", "kra", "dra", dll
    text = re.sub(rf'(?<=\w)r(?=([{DAFTAR_KONSONAN}])([{SEMI_VOKAL}]))', 'ṙ', text)
    # 1. Ubah 'r' menjadi 'ṙ' jika setelahnya konsonan + vokal
    text = re.sub(rf'(?<=\w)r(?=([{DAFTAR_KONSONAN}])({VOKAL_REGEX}))', 'ṙ', text)
    #2. gandakan huruf konsonan setelah ṙ, kecuali yang dalam TIDAK_DIGANDAKAN
    text = re.sub(rf'(?<=ṙ)([{DAFTAR_KONSONAN}])', lambda m: m.group(1) if m.group(1) in TIDAK_DIGANDAKAN else m.group(1) * 2, text)
    # 3. ROLLBACK: Jika sebelum ṙ ada konsonan
    def rollback_if_preceded_by_consonant(match):
        prev = match.group(1)
        kons = match.group(2)
        return f'{prev}r{kons}'
    text = re.sub(rf'([{DAFTAR_KONSONAN}])ṙ([{DAFTAR_KONSONAN}])\2?', rollback_if_preceded_by_consonant, text)
    # ubah kembali ṙ ke r jika setelahnya justru vokal
    text = re.sub(rf'(?<=ṙ)(?={VOKAL_REGEX})', 'r', text)

    # Mahaprana
    for pattern, replacement in HUKUM_ṙ_MAHAPRANA.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    #kasus ry ṙyy
    text = re.sub(
    r'(?:(?<=^)|(?<=\s))ry(?=[^\s-])|(?:\brī\b[^\S\n]+a)', ' ṙyy', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # ganti 'r' jadi ṙ jika diikuti spasi atau tanda hubung
    text = re.sub(r'(?<=\w)r(?=[\s-])', 'ṙ', text)

    # Daftar penggantian spesial
    for pola, ganti in PENGGANTIAN_SPESIAL.items():
        text = re.sub(pola, ganti, text)

    return text

# Fungsi untuk finalisasi (penyesuaian akhir)
def finalisasi(text):
    for pattern, replacement in FINALISASI_PENGGANTI:
        text = pattern.sub(replacement, text)
    return text