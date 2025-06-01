import re
from modul_jtwk.kamus_jtwk import substitutions

# Character sets
VOKAL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûôAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOKAL_KECIL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûô'
KONSONAN = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
SEMI_VOKAL = 'lwyr'
TIDAK_DIGANDAKAN = set('nṅṇhṣscꞓrṙṫŧꝑǥɉƀꝁkdḍḋdđ')

# Pre-compiled regex patterns
REGEX_CACHE = {
    'vokal': re.compile(f'[{VOKAL}]'),
    'vokal_kecil': re.compile(f'[{VOKAL_KECIL}]'),
    'awal_baris_vokal': re.compile(rf'(^|\n)([{VOKAL}])', re.MULTILINE),
    'non_huruf_vokal': re.compile(rf'([^\w\s-])(\s*)([{VOKAL}])'),
    'backtick_vokal': re.compile(rf'`([{VOKAL}])'),
    'substitusi': [(re.compile(p), r) for p, r in substitutions.items()],
}

# Mapping tables
KAPITAL_MAP = str.maketrans('AĀÂIĪÎUŪÛOŌÔEÊÉÈꜽꜷ', 'aāâiīîuūûoōôeêéèꜽꜷ')
VOKAL_KAPITAL = {'ꜽ': 'Ꜽ', 'è': 'È', 'é': 'É'}

# Rule sets
HUKUM_AKSARA_CLUSTER = [
    (r'nḍ', 'ṇḍ'), (r'nḋ', 'ṇḋ'), (r'nṭ', 'ṇṭ'), (r'nṫ', 'ṇṫ'),
    (r'nc', 'ñc'), (r'nj', 'ñj'), (r'ks', 'kṣ'), (r'ꝁs', 'ꝁṣ'),
    (r'gs', 'gṣ'), (r'ǥs', 'ǥṣ'), (r'jn', 'jñ'), (r'rs', 'ṙṣ'),
    (r'ṣt', 'ṣṭ'), (r'sṭ', 'ṣṭ'), (r'ṣŧ', 'ṣṫ'), (r'sry', 'śry'),
    (r'sṫ', 'ṣṫ')
]

# Aturan khusus dengan lambda function
HUKUM_AKSARA_KHUSUS = [
    (re.compile(r'(?<=\w)sṭ(?:h)?(?=\w)'), lambda m: 'ṣṫ' if m.group(0).endswith('h') else 'ṣṭ')
]

HUKUM_ṙ_MAHAPRANA = [
    ('ṙk', 'ṙkk'), ('ṙꝁ', 'ṙkꝁ'), ('ṙṫ', 'ṙṭṫ'), ('ṙꝑ', 'ṙpꝑ'),
    ('ṙǥ', 'ṙgǥ'), ('ṙɉ', 'ṙjɉ'), ('ṙƀ', 'ṙbƀ'), ('ṙṇ', 'ṙṇṇ'),
    ('ṙn', 'ṙṇn'), ('ṙd', 'ṙdd'), ('ṙđ', 'ṙdđ'), ('ṙḍ', 'ṙdḍ'),
    ('ṙḋ', 'ṙdḋ'), ('ṙc', 'ṙcc'), ('ṙꞓ', 'ṙcꞓ')
]

PENGGANTIAN_ṙ = [
    #pengecualian vokal a
    (r'ṙs', 'ṙṣ'), (r'ṛs', 'ṛṣ'), (r'ṙṣik\b', 'ṙsik'), 
    (r'ṙṇny', 'ṙny'), (r'aṙyy([aā])', r'ary\1'),
    (r'(ā|a)ś([cꞓ])ary', r'\1ś\2aṙyy'), (r'ṙyyakĕn', 'ryakĕn'), 
    (r'p(a|ā)ṙśś', r'p\1ṙś'),
    (rf'\b((?!r)[{KONSONAN}])aryan\b', r'\1aṙyyan'),
    (rf'\b(b|h|p|g)arya', r'\1aṙyya'),

    #pengecualian vokal u

    (rf'\b(niṙ|duṙ|pāṙ)([{KONSONAN}])\2([{KONSONAN}])', r'\1\2\3'),
    (r'ṙmmu ', 'ṙmu '), (r'uṙww', 'urw'), 
    (r'kaṙww(a|â|ā)', r'karw\1'),
    (r'tumiṙww(a|â|ā)', 'tumirw\1'),

    #cegah r+zwj-zwnj agar tidal jadi ra pangku 
    (r'r\u200c', 'ṙ'), (r'r\u200d', 'ṙ'),

    #hapus zwj-zwnj 
    (r'\u200c', ''), (r'\u200d', '')
]

def kata_baku(text):
    """Kapitalisasi vokal awal baris dan substitusi kamus"""
    # Kapitalisasi vokal awal baris
    text = REGEX_CACHE['awal_baris_vokal'].sub(
        lambda m: m.group(1) + m.group(2).upper(), text
    )
    
    # Substitusi kamus
    for pattern, replacement in REGEX_CACHE['substitusi']:
        text = pattern.sub(replacement, text)
    
    return text

def hukum_aksara(text):
    """Terapkan hukum aksara Jawa"""
    # Konsonan berdiri di antara spasi
    #Kasus konsonan berdiri diantara spasi
    text = re.sub(rf"([{KONSONAN}])([^\S\n]*|-)([{KONSONAN}])[^\S\n]+([{VOKAL}])", r"\1\2\3-\4", text, flags=re.IGNORECASE)

    # Terapkan aturan hukum aksara biasa
    for pattern, replacement in HUKUM_AKSARA_CLUSTER:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Terapkan aturan khusus dengan lambda function
    for compiled_pattern, replacement_func in HUKUM_AKSARA_KHUSUS:
        text = compiled_pattern.sub(replacement_func, text)
    
    return text

def hukum_ṙ(text):
    """Terapkan hukum ṙ (r dengan titik)"""
    # Bersihkan konsonan ganda setelah ṙ/r (seperti ṙjj → rj)
    text = re.sub(rf'[rṙ]([{KONSONAN}])\1', r'r\1', text)
    
    # Step tambahan untuk kluster seperti "gra", "kra", "dra"
    text = re.sub(rf'(?<=\w)r(?=([{KONSONAN}])([{SEMI_VOKAL}]))', 'ṙ', text)
    
    # 1. Ubah 'r' menjadi 'ṙ' jika setelahnya konsonan + vokal non kapital
    text = re.sub(rf'(?<=\w)r(?=([{KONSONAN}])([{VOKAL_KECIL}]))', 'ṙ', text)
    
    # 2. Gandakan konsonan setelah ṙ (kecuali yang dalam TIDAK_DIGANDAKAN)
    text = re.sub(
        rf'(?<=ṙ)([{KONSONAN}])', 
        lambda m: m.group(1) if m.group(1) in TIDAK_DIGANDAKAN else m.group(1) * 2, 
        text
    )
    
    # 3. ROLLBACK: Jika sebelum ṙ ada konsonan
    text = re.sub(
        rf'([{KONSONAN}])ṙ([{KONSONAN}])\2?',
        lambda m: f'{m.group(1)}r{m.group(2)}', text
    )
    
    # Ubah ṙ kembali ke r jika diikuti vokal
    text = re.sub(rf'ṙ(?=[{VOKAL_KECIL}])', 'r', text)
    
    # Kasus ry -> ṙyy (di awal kata atau setelah spasi/tanda hubung)
    # Pola regex yang digunakan untuk mencari 'ry' yang perlu diganti menjadi 'ṙyy'
    pattern = (
        fr'(?:(?<=[{KONSONAN}]\s)'  # cocok jika didahului konsonan + spasi
        r'|(?<=^)'                 # atau berada di awal baris
        r'|(?<=-))'                # atau setelah tanda hubung '-'
        r'ry(?=[^\s-])'            # dan diikuti huruf (bukan spasi atau tanda hubung)
        r'|(?:\brī\b[^\S\n]+a)'    # atau kasus khusus: rī (kata sendiri) lalu spasi dan 'a'
    )
    
    # Ganti semua pola yang cocok dengan 'ṙyy'
    text = re.sub(pattern, 'ṙyy', text, flags=re.MULTILINE | re.IGNORECASE)
    
    #print(text)  # Debug print seperti kode asli

    # Mahaprana
    for pattern, replacement in HUKUM_ṙ_MAHAPRANA:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Penggantian spesial
    for pattern, replacement in PENGGANTIAN_ṙ:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def hukum_sigeg(text):
    """Terapkan hukum sigeg (tanda akhir kata)"""
    # Penyigegan dasar
    for old, new in [('ṅ', 'ŋ'), ('h', 'ḥ'), ('r', 'ṙ')]:
        text = re.sub(
            rf'(?<!^)(?<!\n){old}\b(?!(?: ?|- ?)[{VOKAL_KECIL}])',
            new, text
        )
    
    # ṅ ulang
    text = re.sub(
        rf'([{KONSONAN}])([{VOKAL_KECIL}])[ŋṅ][-]*(\1)(\2)([ŋṅ])',
        r'\1\2ŋ\3\4\5', text
    )
    
    # Ubah ṙ jadi r di ujung baris/kalimat
    text = re.sub(
        r'ṙ([ \-]*)(.)', 
        lambda m: ('r' if not m.group(2).isalpha() else 'ṙ') + m.group(1) + m.group(2),
        text
    )

    # Kasus khusus
    text = re.sub(r'\s+ŋ\s+h', ' ṅh', text, re.IGNORECASE)
    text = re.sub(rf'kiŋki(ṅ|ŋ)', r'kiṅki\1', text)
    
    return text

def finalisasi(text):
    """Finalisasi dan kapitalisasi"""
    # Kasus spesial pasanyan nya
    text = re.sub(
        rf'([rhṅ])(?=nṇ?y[{VOKAL}])',
        lambda m: {'r': 'ṙ', 'h': 'ḥ', 'ṅ': 'ŋ'}[m.group(1)], text
    )
    
    # Sigeg bertemu sigeg
    text = re.sub(r'ṙ[^\S\n]*ŋ', r'ṙ ṅ', text)
    text = re.sub(r'ḥ[^\S\n]*ŋ', r'ḥ ṅ', text)
    
    # Normalisasi spasi
    text = re.sub(r'[^\S\n]+', ' ', text)
    
    # Kapitalisasi vokal awal baris
    text = REGEX_CACHE['awal_baris_vokal'].sub(
        lambda m: m.group(1) + VOKAL_KAPITAL.get(m.group(2), m.group(2).upper()),
        text
    )
    
    # Kapitalisasi setelah tanda baca
    text = REGEX_CACHE['non_huruf_vokal'].sub(
        lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).upper()}", text
    )
    
    # Kapitalisasi setelah backtick
    text = REGEX_CACHE['backtick_vokal'].sub(
        lambda m: m.group(1).upper(), text
    )
    
    return text