import re
from modul_jtwk.kamus_jtwk import substitutions
from modul_jtwk.konstanta import VOKAL_NON_KAPITAL, DAFTAR_VOKAL, DAFTAR_KONSONAN, SEMI_VOKAL, TIDAK_DIGANDAKAN, VOKAL_PANJANG, SH

# Pre-compiled regex patterns
REGEX_CACHE = {
    'vokal': re.compile(f'[{DAFTAR_VOKAL}]'),
    'vokal_kecil': re.compile(f'[{VOKAL_NON_KAPITAL}]'),
    'awal_baris_vokal': re.compile(rf'(^|\n)([{DAFTAR_VOKAL}])', re.MULTILINE),
    'non_huruf_vokal': re.compile(rf'([^\w\s-])(\s*)([{DAFTAR_VOKAL}])'),
    'backtick_vokal': re.compile(rf'`([{DAFTAR_VOKAL}])'),
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
    (r'sṭ', 'ṣṭ'), (r'ṣŧ', 'ṣṫ'), (r'sry', 'śry'), (r'sṫ', 'ṣṫ'),
    (r'kṣn', 'kṣṇ')
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
    (r'ṙs', 'ṙṣ'), (r'ṙṣik\b', 'ṙsik'), 
    (r'ṙṇny', 'ṙny'), (r'aṙyy([aā])', r'ary\1'),
    (r'(ā|a)ś([cꞓ])ary', r'\1ś\2aṙyy'), (r'ṙyy(akĕn|aku)', r'ry\1'), 
    (r'p(a|ā)ṙśś', r'p\1ṙś'),
    (rf'\b((?!r)[{DAFTAR_KONSONAN}])aryan\b', r'\1aṙyyan'),
    (rf'\b(b|h|p|g)arya', r'\1aṙyya'),

    #cegah setelah nir durpar konsonan tumpuk tiga
    #(rf'\b(niṙ|duṙ|pāṙ([{DAFTAR_KONSONAN}])\2([{DAFTAR_KONSONAN}])', r'\1\2\3'),
    #(rf'ṙ([{DAFTAR_KONSONAN}])\1([{DAFTAR_KONSONAN}])', r'ṙ\1\2'),

    #kata khusus
    #(rf'\bduṙṇn([{DAFTAR_VOKAL}])', r'duṙn\1'), #khusus durnaya
    (rf'mātsyarya', r'mātsyaṙyya'),
    (rf'\bduṙṇn([{DAFTAR_VOKAL}])', r'duṙn\1'), #khusus durnaya
    (rf'(a|ā)ṙwwud(a|ā)', r'\1ṙwud\2'), #khusus arwuda
    (rf'paṙggata', r'paṙgata'), # khusus ghana dari sanskrit, par ghana ta
    (rf'\bhoṙwwi\b', r'horwi'),
    (rf'\bmaṙkkata\b', r'maṙkata'), #hijau
    (rf'\bmaṙbbuk\b', r'maṙbuk'), 
    #(rf'daryas', r'daṙyyas'),

    #pengecualian vokal u
    (r'ṙmmu ', 'ṙmu '), 
    (rf'([{DAFTAR_KONSONAN}])uṙww(a|i|u)', r'\1urw\2'), 
    (r'tumiṙww(a|â|ā)', r'tumirw\1'),
    (r'ṙwwaṅ\b', r'rwaṅ'),
    (rf'([{DAFTAR_KONSONAN.replace('đ','').replace('s','').replace('p','').replace('g','')}])aṙww(a|â|ā)', r'\1arw\2'),

    #cegah r+zwj-zwnj agar tidal jadi ra pangku 
    (r'r\u200c', 'ṙ'), (r'r\u200d', 'ṙ'),(rf'r{SH}', 'ṙ'),
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

    # ṅ ulang
    text = re.sub(
        rf'([{DAFTAR_KONSONAN}])([{VOKAL_NON_KAPITAL}])[ŋṅ][-]*(\1)(\2)([ŋṅ])',
        r'\1\2ŋ\3\4\5', text
    )
    
    
    return text

def hukum_aksara(text):
    """Terapkan hukum aksara Jawa"""
    # Konsonan berdiri di antara spasi
    #Kasus konsonan berdiri diantara spasi
    text = re.sub(rf"([{DAFTAR_KONSONAN}])([^\S\n]*|-)([{DAFTAR_KONSONAN}])[^\S\n]+([{DAFTAR_VOKAL}])", r"\1\2\3-\4", text, flags=re.IGNORECASE)

    # Terapkan aturan hukum aksara biasa
    for pattern, replacement in HUKUM_AKSARA_CLUSTER:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Terapkan aturan khusus dengan lambda function
    for compiled_pattern, replacement_func in HUKUM_AKSARA_KHUSUS:
        text = compiled_pattern.sub(replacement_func, text)
    
    return text

RE_HUKUM_R = [
    # Bersihkan konsonan ganda setelah ṙ/r (ṙjj → rj)
    #(re.compile(rf'[rṙ]([{DAFTAR_KONSONAN}])\1'), r'r\1'),

    # Step tambahan untuk kluster seperti "gra", "kra", "dra"
    (re.compile(rf'(?<=\w)r(?=([{DAFTAR_KONSONAN}])([{SEMI_VOKAL}]))'), 'ṙ'),

    # Ubah 'r' jadi 'ṙ' jika setelahnya konsonan + vokal non kapital
    (re.compile(rf'(?<=\w)r(?=([{DAFTAR_KONSONAN}])+([{VOKAL_NON_KAPITAL}]))'), 'ṙ'),

    # ROLLBACK: jika sebelum ṙ ada konsonan
    (re.compile(rf'([{DAFTAR_KONSONAN}])ṙ([{DAFTAR_KONSONAN}])\2?'), r'\1r\2'),

    # ṙ kembali ke r jika diikuti vokal
    (re.compile(rf'ṙ(?=[{VOKAL_NON_KAPITAL}])'), 'r'),

    # Kasus ry awal kata / setelah spasi / tanda hubung / kata rī
    (re.compile(
        fr'(?:(?<=\w\s)|(?<=^)|(?<=-))ry(?=[^\s-])|(?:\brī\b[^\S\n]+a)',
        re.MULTILINE | re.IGNORECASE
    ), 'ṙyy'),

    # Kasus ry + satu vokal
    (re.compile(rf' ry([{DAFTAR_VOKAL}])\b', re.IGNORECASE), r' ṙyy\1'),
]


def hukum_ṙ(text):
    """Terapkan hukum ṙ (r dengan titik)"""
    # Jalankan regex sederhana secara berurutan
    for regex, repl in RE_HUKUM_R:
        text = regex.sub(repl, text)

    # Gandakan konsonan setelah ṙ, kecuali dalam TIDAK_DIGANDAKAN
    
    text = re.sub(
        rf'(?<=ṙ)([{DAFTAR_KONSONAN}])(?![{DAFTAR_KONSONAN}])',
        lambda m: m.group(1) if m.group(1) in TIDAK_DIGANDAKAN else m.group(1) * 2,
        text,
    )
    '''
    text = re.sub(
        rf'(?<=ṙ)([{DAFTAR_KONSONAN}])',
        lambda m: m.group(1) if m.group(1) in TIDAK_DIGANDAKAN else m.group(1) * 2,
        text,
    )
    '''

    # Mahaprana dan penggantian spesial
    for pattern, replacement in HUKUM_ṙ_MAHAPRANA + PENGGANTIAN_ṙ:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


# --- Regex hukum sigeg (precompiled, gaya hukum_ṙ) ---
SPECIFIC_FOLLOWING = r'(?:lĕ|rĕ|ḷ|ṛ)'  # Pola khusus setelah 'ṅ'

RE_HUKUM_SIGEG = [
    # Kriteria 3: Vokal Panjang + ' ṅ ' + pola khusus -> ' ṅ-'
    (re.compile(rf'(?<=[{VOKAL_PANJANG}]) ṅ (?={SPECIFIC_FOLLOWING})'), r' ṅ-'),

    # Kriteria 1: Vokal + ' ṅ ' + Konsonan -> '-ŋ '
    (re.compile(rf'(?<=[{DAFTAR_VOKAL}]) ṅ (?=[{DAFTAR_KONSONAN}])'), r'-ŋ '),

    # Kriteria 2: Konsonan + ' ṅ ' + Konsonan -> ' ṅ '
    (re.compile(rf'(?<=[{DAFTAR_KONSONAN}]) ṅ (?=[{DAFTAR_KONSONAN}])'), r' ṅ '),

    # Kriteria 4: Vokal + ' ṅ ' + Vokal -> ' ṅ-'
    (re.compile(rf'(?<=[{DAFTAR_VOKAL}]) ṅ (?=[{DAFTAR_VOKAL}])'), r' ṅ-'),

    # ṅ di akhir kata tanpa vokal sesudahnya → ŋ
    (re.compile(rf'(?<!^)(?<!\n)(?<=\w|-)ṅ\b(?!-)(?!(?: ?|- ?)[{DAFTAR_VOKAL}])'), 'ŋ'),

    # Kriteria 5: vokal + ṅ - konsonan
    (re.compile(rf'(?<=[{DAFTAR_VOKAL}])ṅ-(?=[{DAFTAR_KONSONAN}])'), r'ŋ-'),

    # Kriteria 6: konsonan + ṅ + h
    (re.compile(rf'(?<=[{DAFTAR_KONSONAN}])[^\S\n]+ṅ[^\S\n]+h'), r' ṅh'),
]


def hukum_sigeg(text):
    """Terapkan hukum sigeg (tanda akhir kata)"""

    # Jalankan semua regex utama (precompiled)
    for regex, repl in RE_HUKUM_SIGEG:
        text = regex.sub(repl, text)

    # Ganti untuk 'h' dan 'r' sesuai aturan sebelumnya
    for old, new in [('h', 'ḥ'), ('r', 'ṙ')]:
        text = re.sub(
            rf'(?<!^)(?<!\n){old}\b(?!(?: ?|- ?)[{VOKAL_NON_KAPITAL}])',
            new, text
        )

    # Ubah ṙ jadi r di ujung baris/kalimat
    text = re.sub(
        r'ṙ([ \-~$]*)(.)',
        lambda m: ('r' if not m.group(2).isalpha() else 'ṙ') + m.group(1) + m.group(2),
        text
    )
    text = re.sub(r'ṙ *$', r'r', text)

    # Kasus khusus
    text = re.sub(r'\s+ŋ\s+h', ' ṅh', text, re.IGNORECASE)
    text = re.sub(rf'kiŋki(ṅ|ŋ)', r'kiṅki\1', text)

    return text



# Kumpulan regex finalisasi — dijalankan berurutan
RE_FINALISASI = [
    # 1️⃣ Normalisasi spasi
    (re.compile(r'[^\S\n]+'), ' '),

    # 2️⃣ Kasus spesial pasanyan nya
    (re.compile(rf'([rhṅ])(?=nṇ?y[{DAFTAR_VOKAL}])'),
     lambda m: {'r': 'ṙ', 'h': 'ḥ', 'ṅ': 'ŋ'}[m.group(1)]),

    # 3️⃣ Huruf + spasi + vokal kapital
    (re.compile(rf'(h|ṅ|r)(\s|-)([{VOKAL_KAPITAL}])'),
     lambda m: {'h': 'ḥ', 'ṅ': 'ŋ', 'r': 'ṙ'}[m.group(1)] + m.group(2) + m.group(3)),

    # 4️⃣ Sigeg bertemu sigeg
    (re.compile(r'ṙ[^\S\n]*ŋ'), 'ṙ ṅ'),
    (re.compile(r'ḥ[^\S\n]*ŋ'), 'ḥ ṅ'),

    # 5️⃣ Vokal diapit spasi → vokal dihubung tanda -
    (re.compile(rf' ([{DAFTAR_VOKAL}]) '), r' \1-'),

    # 6️⃣ Konsonan non-ṅḥṙ berdiri di antara spasi
    #    6a. vokal + spasi + konsonan tunggal
    (re.compile(rf'([{DAFTAR_VOKAL}]) (\b(?![ṅḥṙ])[{DAFTAR_KONSONAN}]\b) '),
     r'\1-\2 '),
    #    6b. konsonan tunggal + spasi + vokal
    (re.compile(rf' (\b(?![ṅḥṙ])[{DAFTAR_KONSONAN}]\b) ([{DAFTAR_VOKAL}])'),
     r'\1-\2 '),

    # 7️⃣ Pengulangan
    (re.compile(r'\b(\w{3,})\s+\1\b'), r'\1-\1'),
    (re.compile(r'\b(\w*?)(\w{3,})\s+\2(\w+)\b'), r'\1\2-\2\3'),
    (re.compile(r'\b(\w+)\s+\1(\w+)\b'), r'\1-\1\2'),
]


def finalisasi_jtwk(text):
    """Finalisasi dan kapitalisasi"""
    # Jalankan semua regex substitusi
    for regex, repl in RE_FINALISASI:
        text = regex.sub(repl, text)

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