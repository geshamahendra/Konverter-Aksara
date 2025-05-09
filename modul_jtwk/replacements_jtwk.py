import re

# Set transliterasi untuk berbagai mode
replacements = {
    'kinanti': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        'ᶇ': 'ŋ', 'ᶆ': 'ṃ', 'ꞕ': 'ḥ', 'ᶉ': 'ṙ', 
        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'ĕ','E' : 'Ĕ','sh' : 'ś','ss' : 'ṣ',
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
    'normal': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'ĕ','E' : 'Ĕ','sh' : 'ś','ss' : 'ṣ',
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
        'kakawin': {
        'ng': 'ṅ',
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ',
        'ai': 'ꜽ', 'au': 'ꜷ', 
        #'-' : ' ', 
        'Ç' : 'Ś', 'ç' : 'ś',
        '’' : '0‍',
        '‘' : '0‍',

        "x" : 'ś', "f" : 'ṣ', "t'" : 'ṭ', "d'" : 'ḍ', "q" : 'ĕ', "n`" : 'ñ', "n'" : 'ṇ', "o'" : 'ö',
        
        'v' : 'w',
        #'ṁ' : 'ŋ',
        'ṃ' : 'ŋ',  'ṁ' : 'ŋ',
        #'sh' : 'ś','ss' : 'ṣ',

        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ', 'Om̃' : 'Ōṃ',
    },
    'lampah': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        '-' : ' ',
        '’' : '0‍',
        'v' : 'w',
        'ṁ' : 'ŋ',
        

        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'è','E' : 'È', 'ê' : 'è', 'Ê' : 'È',#'sh' : 'ś','ss' : 'ṣ',
        'â':'ā', 'î':'ī', 
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
    'jawa': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'ĕ','E' : 'Ĕ','sh' : 'ś','ss' : 'ṣ',
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
    'pali': {
        'E': 'È',  # Pali specific replacement
        'e': 'è',  # Pali specific replacement
        'kh': 'ꝁ', 'gh': 'ǥ', 'ch': 'ꞓ', 'jh': 'ɉ',
        'ṭh': 'ṭ', 'ḍh': 'ḋ', 'th': 'ŧ', 'dh': 'đ',
        'ph': 'ꝑ', 'bh': 'ƀ', 'ḷi': 'ḹ', ';': ':',
    },
    'sastra_org': {
        'kh': 'ꝁ', 'gh': 'ǥ',
        'ch': 'ꞓ', 'jh': 'ɉ',
        'th': 'ṭ', 'dh': 'ḍ',
        'ph': 'ꝑ', 'bh': 'ƀ',

        'ê' : 'ĕ', 'Ê' : 'Ĕ',
        'e' : 'è', 'E': 'È',
        'le': 'ḷ', 'ṛe': 'ṛ', 'ia' : 'y',
    },
    'sriwedari': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'ḍ',
        'ph': 'ꝑ','bh': 'ƀ', 'ny': 'ñ', 'iè': 'iyè',

        'ê' : 'ĕ', 'Ê' : 'Ĕ',
        'e' : 'ĕ', 'E': 'Ĕ',
        'é' : 'è', 'É' : 'È', 
        'le': 'ḷ', 'ṛe': 'ṛ', 'ia' : 'ya',
    },
    'satya': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ṭ','dh': 'ḍ',
        'ph': 'ꝑ','bh': 'ƀ', 'ny': 'ñ', 'iè': 'iyè',

        'ê' : 'ĕ', 'Ê' : 'Ĕ',
        'e' : 'è', 'E': 'Ĕ',
        #'é' : 'è', 'É' : 'È', 
        'le': 'ḷ', 'ṛe': 'ṛ', 'ia' : 'ya',
        '-': '',
    },
    'cerita': {
        'kh': 'ḳ', 'ua' : 'wa', 'ia' : 'ya',
        'gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ', 'ny' : 'ñ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ṭ','dh': 'ḍ',
        'ph': 'ꝑ','bh': 'ƀ', #'ny': 'ñ',

        'e' : 'ĕ','E' : 'Ĕ',
    },
        'sanskrit': {
        #'E': 'È',  # Pali specific replacement
        'e': 'è',  # Pali specific replacement
        'kh': 'ꝁ', 'gh': 'ǥ', 'ch': 'ꞓ', 'jh': 'ɉ',
        'ṭh': 'ṭ', 'ḍh': 'ḋ', 'th': 'ŧ', 'dh': 'đ',
        'ph': 'ꝑ', 'bh': 'ƀ', 'ḷi': 'ḹ', 
        'v': 'w', 'ai' : 'ꜽ', 'au' : 'ꜷ', 'oṃ':'Ōṃ', 'Oṁ':'Ōṃ', 'Om̃':'Ōṃ',
        "'" : "0", "’" : "0", 'ṃ' : 'ŋ', 'ṁ' : 'ŋ'
    }
}

# Mode kakawin mewarisi mode normal dan menambahkan/menimpa beberapa entri
#replacements['lampah'] = replacements['kakawin'].copy()
replacements['modern_lampah'] = replacements['sriwedari'].copy()
#replacements['satya'] = replacements['sriwedari'].copy()

def replace_numbers_with_colon(text):
    text = re.sub(r'([\dA-Za-z]+[/\\][\dA-Za-z]+[/\\][\dA-Za-z]+)', r':\1:', text)
    return text

'''
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

ZWNJ = '\u200C'
VOWELS = 'aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOWELS_PATTERN = f'[{VOWELS}]'

def get_clean_metrum(metrum_line):
    metrum_line = metrum_line.replace('-', '–')
    return [c for c in metrum_line if c in ['–', '⏑', '⏓']]

def hitung_jumlah_metrum(line):
    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = re.sub(r'[\u200C\u200D\s]', '', isi)
            jumlah_dalam_blok = len(re.findall(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = line[:match.start()] + line[match.end():]
            jumlah_di_luar = len(re.findall(r'[–⏑⏓]', baris_di_luar))
            return (jumlah_dalam_blok * perkalian) + jumlah_di_luar
    return len(re.findall(r'[–⏑⏓]', line))

def process_vowel_pair(match, metrum, line):
    v1, space, v2 = match.groups() if len(match.groups()) == 3 else (match.group(1), '', match.group(2))
    vokal_indices = [i for i, c in enumerate(line) if c in VOWELS]
    v1_pos_in_line = match.start()
    v2_pos_in_line = match.start(len(match.groups()))
    try:
        v1_idx = next(i for i, idx in enumerate(vokal_indices) if idx == v1_pos_in_line)
        v2_idx = next(i for i, idx in enumerate(vokal_indices) if idx == v2_pos_in_line)
    except StopIteration:
        return f"{v1}{space}{v2}"
    met1 = metrum[v1_idx % len(metrum)]
    met2 = metrum[v2_idx % len(metrum)]
    if met1 == '⏑' and met2 == '⏑':
        return f"{v1}{space}{ZWNJ}{v2.upper()}"
    else:
        return f"{v1}{space}{v2}"

def tandai_vokal_pendek_dalam_pasangan(text):
    lines = text.splitlines()
    hasil = []
    metrum = None

    for line in lines:
        line_strip = line.strip()

        if line_strip.startswith("<") and ":" in line_strip:
            hasil.append(line)  # biarkan baris seperti <Basantatilaka>:2. tetap
            continue

        if re.search(r'[–⏑⏓]', line_strip):
            metrum = get_clean_metrum(line_strip)
            jumlah = hitung_jumlah_metrum(line_strip)
            hasil.append(f"{line_strip} : {jumlah}")
            continue

        if not metrum or len(metrum) == 0:
            hasil.append(line)
            continue

        jumlah_vokal = len(re.findall(VOWELS_PATTERN, line))
        if jumlah_vokal != len(metrum):
            hasil.append(line)
            continue

        line = re.sub(
            f'({VOWELS_PATTERN})(\\s+)({VOWELS_PATTERN})',
            lambda m: process_vowel_pair(m, metrum, line),
            line
        )
        line = re.sub(
            f'({VOWELS_PATTERN})({VOWELS_PATTERN})',
            lambda m: process_vowel_pair(m, metrum, line),
            line
        )

        hasil.append(line)

    return '\n'.join(hasil)
'''
'''
import re

# Kompilasi regex untuk performa
RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ]')

ZWNJ = '\u200C'
VOWELS = 'aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOWEL_PENDEK = 'aiuĕo'
VOWEL_PANJANG = 'āâîīûūêôeèéöĀÂÎĪÛŪÊÔÉÈÖŌ'

# Fungsi bantu untuk bersihkan karakter tak terlihat
def bersihkan_karakter_tak_terlihat(teks):
    return re.sub(r'[\u200C\u200D\s]', '', teks)

# Fungsi untuk menghitung simbol metrum
def process_baris(baris):
    if not RE_METRUM_SIMBOL.search(baris):
        return baris

    if "[" in baris and "]" in baris:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', baris)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = baris[:match.start()] + baris[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            jumlah_total = (jumlah_dalam_blok * perkalian) + jumlah_di_luar
        else:
            jumlah_total = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris))
    else:
        jumlah_total = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris))

    return baris.rstrip() + f" : {jumlah_total}"

def get_clean_metrum(line):
    line = line.replace('-', '–')
    hasil = []

    def extract_metrum_segment(segment):
        return [c for c in segment if c in ['–', '⏑', '⏓']]

    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            blok = extract_metrum_segment(isi) * perkalian
            line_di_luar = line[:match.start()] + line[match.end():]
            luar = extract_metrum_segment(line_di_luar)
            return luar[:match.start()] + blok + luar[match.end():]
    return [c for c in line if c in ['–', '⏑', '⏓']]

def hitung_jumlah_metrum(line):
    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = line[:match.start()] + line[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            return (jumlah_dalam_blok * perkalian) + jumlah_di_luar
    return sum(1 for _ in RE_METRUM_SIMBOL.finditer(line))

def tandai_vokal_pendek_dalam_pasangan(text):
    # Fungsi ini bersifat non-rekursif dan diasumsikan tidak ada lebih dari satu pasangan vokal yang berhimpitan berurutan.
    lines = text.splitlines()
    hasil = []
    metrum = None

    for line in lines:
        line_strip = line.strip()

        if line_strip.startswith("<") and ":" in line_strip:
            hasil.append(line)
            continue

        if RE_METRUM_SIMBOL.search(line_strip):
            metrum = get_clean_metrum(line_strip)
            jumlah = hitung_jumlah_metrum(line_strip)
            hasil.append(f"{line_strip} : {jumlah}")
            continue

        if not metrum or len(metrum) == 0:
            hasil.append(line)
            continue

        vokal_matches = list(RE_VOKAL.finditer(line))
        if len(vokal_matches) != len(metrum):
            hasil.append(line)
            continue

        hasil_line = list(line)
        skip_next = False

        for i in range(len(vokal_matches) - 1):
            if skip_next:
                skip_next = False
                continue

            m1, m2 = vokal_matches[i], vokal_matches[i + 1]
            v1, v2 = m1.group(), m2.group()
            idx1, idx2 = m1.start(), m2.start()
            met1, met2 = metrum[i], metrum[i + 1]

            if idx2 - idx1 <= 2:
                if line[idx1+1:idx2].isspace() or idx2 == idx1 + 1:
                    if met1 == '⏑' and met2 == '⏑':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True
                    elif (
                        (v1 in VOWEL_PANJANG and v2 in VOWEL_PENDEK and met1 == '–' and met2 == '⏑') or
                        (v1 in VOWEL_PENDEK and v2 in VOWEL_PANJANG and met1 == '⏑' and met2 == '–')
                    ):
                        if v1 in VOWEL_PENDEK:
                            hasil_line[m1.start()] = ZWNJ + v1.upper()
                        else:
                            hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True

        hasil.append(''.join(hasil_line))

    return '\n'.join(hasil)
'''

'''
Versi 2
import re

# Kompilasi regex untuk performa
RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ]')

ZWNJ = '\u200C'
VOWELS = 'aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOWEL_PENDEK = 'aiuĕo'
VOWEL_PANJANG = 'āâîīûūêôeèéöĀÂÎĪÛŪÊÔÉÈÖŌ'

# Fungsi bantu untuk bersihkan karakter tak terlihat
def bersihkan_karakter_tak_terlihat(teks):
    return re.sub(r'[\u200C\u200D\s]', '', teks)

# Fungsi untuk menghitung simbol metrum
def process_baris(baris):
    if not RE_METRUM_SIMBOL.search(baris):
        return baris

    if "[" in baris and "]" in baris:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', baris)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = baris[:match.start()] + baris[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            jumlah_total = (jumlah_dalam_blok * perkalian) + jumlah_di_luar
        else:
            jumlah_total = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris))
    else:
        jumlah_total = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris))

    return baris.rstrip() + f" : {jumlah_total}"

def get_clean_metrum(line):
    line = line.replace('-', '–')
    hasil = []

    def extract_metrum_segment(segment):
        return [c for c in segment if c in ['–', '⏑', '⏓']]

    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            blok = extract_metrum_segment(isi) * perkalian
            line_di_luar = line[:match.start()] + line[match.end():]
            luar = extract_metrum_segment(line_di_luar)
            return luar[:match.start()] + blok + luar[match.end():]
    return [c for c in line if c in ['–', '⏑', '⏓']]

def hitung_jumlah_metrum(line):
    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = line[:match.start()] + line[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            return (jumlah_dalam_blok * perkalian) + jumlah_di_luar
    return sum(1 for _ in RE_METRUM_SIMBOL.finditer(line))

def tandai_vokal_pendek_dalam_pasangan(text):
    lines = text.splitlines()
    hasil = []
    metrum = None

    for line in lines:
        line_strip = line.strip()

        if line_strip.startswith("<") and ":" in line_strip:
            hasil.append(line)
            continue

        if RE_METRUM_SIMBOL.search(line_strip):
            metrum = get_clean_metrum(line_strip)
            jumlah = hitung_jumlah_metrum(line_strip)
            hasil.append(f"{line_strip} : {jumlah}")
            continue

        if not metrum or len(metrum) == 0:
            hasil.append(line)
            continue

        vokal_matches = list(RE_VOKAL.finditer(line))
        if len(vokal_matches) != len(metrum):
            hasil.append(line)
            continue

        hasil_line = list(line)
        skip_next = False

        for i in range(len(vokal_matches) - 1):
            if skip_next:
                skip_next = False
                continue

            m1, m2 = vokal_matches[i], vokal_matches[i + 1]
            v1, v2 = m1.group(), m2.group()
            idx1, idx2 = m1.start(), m2.start()
            met1, met2 = metrum[i], metrum[i + 1]

            if idx2 - idx1 <= 2:
                if line[idx1+1:idx2].isspace() or idx2 == idx1 + 1:
                    if met1 == '⏑' and met2 == '⏑':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True
                    elif v1 in VOWEL_PENDEK and v2 in VOWEL_PANJANG and met1 == '⏑' and met2 == '–':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True
                    elif v1 in VOWEL_PANJANG and v2 in VOWEL_PENDEK and met1 == '–' and met2 == '⏑':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True

        hasil.append(''.join(hasil_line))

    return '\n'.join(hasil)
'''
import re

# Kompilasi regex untuk performa
RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ]')
RE_KONSONAN = re.compile(r'[^aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ\s\u200C\u200D]')

ZWNJ = '\u200C'
VOWELS = 'aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOWEL_PENDEK = 'aiuĕ'
VOWEL_PANJANG = 'āâîīûūêôeèéoöꜽꜷĀÂÎĪÛŪÊÔÉÈÖŌꜼꜶ'

# Fungsi bantu untuk bersihkan karakter tak terlihat
def bersihkan_karakter_tak_terlihat(teks):
    return re.sub(r'[\u200C\u200D\s]', '', teks)

# Fungsi untuk menghitung simbol metrum
def process_baris(baris):
    if not RE_METRUM_SIMBOL.search(baris):
        return baris

    if "[" in baris and "]" in baris:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', baris)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = baris[:match.start()] + baris[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            jumlah_total = (jumlah_dalam_blok * perkalian) + jumlah_di_luar
        else:
            jumlah_total = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris))
    else:
        jumlah_total = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris))

    return baris.rstrip() + f" : {jumlah_total}"

def get_clean_metrum(line):
    line = line.replace('-', '–')
    hasil = []

    def extract_metrum_segment(segment):
        return [c for c in segment if c in ['–', '⏑', '⏓']]

    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            blok = extract_metrum_segment(isi) * perkalian
            line_di_luar = line[:match.start()] + line[match.end():]
            luar = extract_metrum_segment(line_di_luar)
            return luar[:match.start()] + blok + luar[match.end():]
    return [c for c in line if c in ['–', '⏑', '⏓']]

def hitung_jumlah_metrum(line):
    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\-\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = line[:match.start()] + line[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            return (jumlah_dalam_blok * perkalian) + jumlah_di_luar
    return sum(1 for _ in RE_METRUM_SIMBOL.finditer(line))

def tandai_vokal_pendek_dalam_pasangan(text):
    lines = text.splitlines()
    hasil = []
    metrum = None

    for line in lines:
        line_strip = line.strip()

        if line_strip.startswith("<") and ":" in line_strip:
            hasil.append(line)
            continue

        if RE_METRUM_SIMBOL.search(line_strip):
            metrum = get_clean_metrum(line_strip)
            jumlah = hitung_jumlah_metrum(line_strip)
            hasil.append(f"{line_strip} : {jumlah}")
            continue

        if not metrum or len(metrum) == 0:
            hasil.append(line)
            continue

        vokal_matches = list(RE_VOKAL.finditer(line))
        if len(vokal_matches) != len(metrum):
            hasil.append(line)
            continue

        hasil_line = list(line)
        skip_next = False

        for i in range(len(vokal_matches) - 1):
            if skip_next:
                skip_next = False
                continue

            m1, m2 = vokal_matches[i], vokal_matches[i + 1]
            v1, v2 = m1.group(), m2.group()
            v1_lower, v2_lower = v1.lower(), v2.lower()
            idx1, idx2 = m1.start(), m2.start()
            met1, met2 = metrum[i], metrum[i + 1]

            # Aturan lama untuk dua vokal bersebelahan atau hanya dipisah spasi
            if idx2 - idx1 <= 2:
                if line[idx1+1:idx2].isspace() or idx2 == idx1 + 1:
                    if met1 == '⏑' and met2 == '⏑':
                        if v1_lower in VOWEL_PENDEK and v2_lower in VOWEL_PENDEK:
                            hasil_line[m2.start()] = ZWNJ + v2.upper()
                            skip_next = True
                    elif v1_lower in VOWEL_PENDEK and v2_lower in VOWEL_PANJANG and met1 == '⏑' and met2 == '–':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True
                    elif v1_lower in VOWEL_PANJANG and v2_lower in VOWEL_PENDEK and met1 == '–' and met2 == '⏑':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True

            # Aturan baru: nada panjang, satu konsonan, spasi, lalu vokal awal kata
            elif met1 == '–' and v1 in VOWEL_PENDEK:
                kata_kata = re.finditer(r'\S+', line)
                kata_list = [(m.start(), m.end(), m.group()) for m in kata_kata]

                kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)

                if (kata_v1 and kata_v2 and kata_v1 != kata_v2 and 
                    RE_VOKAL.match(kata_v2[2][0])):

                    bagian_setelah_v1 = kata_v1[2][kata_v1[2].find(v1) + 1:]
                    konsonan_setelah_v1 = []
                    for char in bagian_setelah_v1:
                        if char in VOWELS:
                            break
                        if RE_KONSONAN.match(char):
                            konsonan_setelah_v1.append(char)

                    if len(konsonan_setelah_v1) == 1 and konsonan_setelah_v1[0] not in 'ṅŋḥṙ':
                        hasil_line[m2.start()] = ZWNJ + v2.upper()
                        skip_next = True

        hasil.append(''.join(hasil_line))

    return '\n'.join(hasil)
