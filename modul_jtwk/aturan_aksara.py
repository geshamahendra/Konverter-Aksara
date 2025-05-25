#Menghapus spasi ada di aturan aksara
import re

# Peta karakter Latin ke aksara Jawa (dalam bentuk dimatikan secara default)
aksara = {
    # Kaṇṭhya
    **{huruf: 'ꦏ꧀' for huruf in ('k', 'K')},
    **{huruf: 'ꦑ꧀' for huruf in ('ꝁ', 'Ꝁ')},
    **{huruf: 'ꦒ꧀' for huruf in ('g', 'G')},
    **{huruf: 'ꦓ꧀' for huruf in ('ǥ', 'Ǥ')},
    **{huruf: 'ꦔ꧀' for huruf in ('ṅ', 'Ṅ')},
    **{huruf: 'ꦲ꧀' for huruf in ('ʰ', 'h', 'H')},
    # Tālawya
    **{huruf: 'ꦕ꧀' for huruf in ('c', 'C')},
    **{huruf: 'ꦖ꧀' for huruf in ('ꞓ', 'Ꞓ')},
    **{huruf: 'ꦗ꧀' for huruf in ('j', 'J')},
    **{huruf: 'ꦙ꧀' for huruf in ('ɉ', 'Ɉ')},
    **{huruf: 'ꦚ꧀' for huruf in ('ñ', 'Ñ')},
    **{huruf: 'ꦯ꧀' for huruf in ('ś', 'Ś', 'ç', 'Ç')},
    **{huruf: 'ꦪ꧀' for huruf in ('y', 'Y')},
    # Mūrdhanya
    **{huruf: 'ꦛ꧀' for huruf in ('ṭ', 'Ṭ')},
    **{huruf: 'ꦜ꧀' for huruf in ('ṫ', 'Ṫ')},
    **{huruf: 'ꦝ꧀' for huruf in ('ḍ', 'Ḍ')},
    **{huruf: 'ꦞ꧀' for huruf in ('ḋ', 'Ḋ')},
    **{huruf: 'ꦟ꧀' for huruf in ('ṇ', 'Ṇ')},
    **{huruf: 'ꦰ꧀' for huruf in ('ṣ', 'Ṣ')},
    **{huruf: 'ꦫ꧀' for huruf in ('r', 'R')},
    # Dantya
    **{huruf: 'ꦠ꧀' for huruf in ('t', 'T')},
    **{huruf: 'ꦡ꧀' for huruf in ('ŧ', 'Ŧ')},
    **{huruf: 'ꦢ꧀' for huruf in ('d', 'D')},
    **{huruf: 'ꦣ꧀' for huruf in ('đ', 'Đ')},
    **{huruf: 'ꦤ꧀' for huruf in ('n', 'N')},
    **{huruf: 'ꦱ꧀' for huruf in ('s', 'S')},
    **{huruf: 'ꦭ꧀' for huruf in ('l', 'L')},
    # Oṣṭhya
    **{huruf: 'ꦥ꧀' for huruf in ('p', 'P')},
    **{huruf: 'ꦦ꧀' for huruf in ('ꝑ', 'Ᵽ')},
    **{huruf: 'ꦧ꧀' for huruf in ('b', 'B')},
    **{huruf: 'ꦨ꧀' for huruf in ('ƀ', 'Ƀ')},
    **{huruf: 'ꦩ꧀' for huruf in ('m', 'M')},
    **{huruf: 'ꦮ꧀' for huruf in ('w', 'W')},
    **{huruf: 'ꦘ꧀' for huruf in ('z', 'Z')},
    # Rĕkan
    **{huruf: 'ꦘ꧀' for huruf in ('z', 'Z')},    
    **{huruf: 'ꦥ꦳꧀' for huruf in ('f', 'F')},    
    **{huruf: 'ꦮ꦳꧀' for huruf in ('v', 'V')},
    **{huruf: 'ꦏ꦳꧀' for huruf in ('ḳ', 'Ḳ')},    
}
sandhangan = {
    'a': '',  # tidak ada sandhangan untuk 'a'
    'i': 'ꦶ',
    'u': 'ꦸ',
    'ꜽ': 'ꦻ',
    'ꜷ': 'ꦻꦴ',
    **{tanda: 'ꦹ' for tanda in ('ū', 'û')},
    **{tanda: 'ꦴ' for tanda in ('ā', 'â')},
    **{tanda: 'ꦼꦴ' for tanda in ('ö', 'ŏ')},
    **{tanda: 'ꦷ' for tanda in ('ī', 'î')},
    **{tanda: 'ꦼ' for tanda in ('ĕ')}, 
    **{tanda: 'ꦺꦴ' for tanda in ('o', 'ô')}, 
    **{tanda: 'ꦺ' for tanda in ('è', 'é', 'e', 'ê')}, 
    **{tanda: 'ꦀ' for tanda in ('ṃ', 'm̃', 'ᶆ', 'ṁ')}, 
    **{tanda: 'ꦁ' for tanda in ('ŋ', 'ᶇ')}, 
    **{tanda: 'ꦃ' for tanda in ('ḥ', 'ꞕ')}, 
    **{tanda: 'ꦂ' for tanda in ('ṙ', 'ᶉ')},
}
swara = {
    # Swara
    'A': 'ꦄ', 'Ā': 'ꦄꦴ', 'I': 'ꦅ', 'Ī': 'ꦇ', 'U': 'ꦎ', 'Ū': 'ꦎꦴ', 'O': 'ꦈ',
    'Ꜷ': 'ꦈꦴ', 'Ꜽ': 'ꦍ', 'Ö': 'ꦄꦼꦴ',
    
    **{bunyi: 'ꦄꦴ' for bunyi in ('Ā', 'Â')},
    **{bunyi: 'ꦇ' for bunyi in ('Ī', 'Î')},
    **{bunyi: 'ꦎꦴ' for bunyi in ('Ū', 'Û')},
    **{bunyi: 'ꦈ' for bunyi in ('Ō', 'Ô')},
    **{bunyi: 'ꦌ' for bunyi in ('E', 'È','É')},
    **{bunyi: 'ꦄꦼ' for bunyi in ('Ĕ')},
    **{bunyi: 'ꦈꦴ' for bunyi in ('Ŏ', 'Ō')},
    # Swara spesial
    **{bunyi: 'ꦉ' for bunyi in ('ṛ', 'Ṛ')},
    **{bunyi: 'ꦉꦴ' for bunyi in ('ṝ', 'Ṝ')},
    **{bunyi: 'ꦊ' for bunyi in ('ḷ', 'Ḷ')},
    **{bunyi: 'ꦋ' for bunyi in ('ḹ', 'Ḹ')},
}
simbol = {
     # Simbol lainnya 
    '1': '꧑', '2': '꧒', '3': '꧓', '4': '꧔', '5': '꧕', '6': '꧖', '7': '꧗', '8': '꧘', '9': '꧙', '0': '꧐',  
    '.': '꧉', ',': '꧈', ']': '꧊', '[': '꧋',
    '(': '꧌', ')': '꧍', 
    '<': '꧁', '>': '꧂',
    '{': '꧁', '}': '꧂', # untuk sub pupuh
    ':': '꧇', '*': '꧄', '@': '꧄', '#' : '꧄꧐꧄', '$' : '꧅', 
    '%' : '\u200B꧄‍꧉ꦧ꧀ꦖ꧉꧄‍\u200B', '^' : '\u200B꧄‍꧉ꦟ꧀ꦢꦿ꧉꧄‍\u200B', '&' : '\u200B꧄‍꧉ꦅ꧉꧄‍\u200B'
}
penyeragaman_vokal = {
    'â': 'ā',
    'î': 'ī',
    'ô': 'o',
    'ê': 'e',
    'è': 'e',
    'û': 'ū',
    'lĕ': 'ḷ',
    'ḷĕ': 'ḷ',
    'lö': 'ḹ',
    'ḹö': 'ḹ',
    'rĕ': 'ṛ',
    'ṛĕ': 'ṛ',
    'rö': 'ṝ',
    'ṝö': 'ṝ'
}

def ganti_tanda_metrum(hasil):
    def ganti_tanda(match):
        baris = match.group()
        baris = re.sub(r'꧋[\u200C\u200D]*', '[', baris)
        baris = re.sub(r'꧊[\u200C\u200D]*', ']', baris)
        return baris

    hasil = re.sub(r'^.*[–⏑⏓].*꧋[\u200C\u200D]*.*$', ganti_tanda, hasil, flags=re.MULTILINE)
    hasil = re.sub(r'^.*[–⏑⏓].*꧊[\u200C\u200D]*.*$', ganti_tanda, hasil, flags=re.MULTILINE)
    hasil = hasil.replace("]×","] × ")
    return hasil

def insert_zwnj_between_consonants(text):
    # Pola pencocokan: konsonan + spasi + konsonan + konsonan
    pattern = r'([bcdfghjklmnpqstvzɉḋḍŧṭṣñṇṅŋꝁǥꞓƀśʰ])[^\S\n]*([ybcdfghjklmnqtvwzɉḋḍŧṭñṇṅŋꝁǥꞓƀśʰ])[^\S\n]*([ḷḹbcdfghjklmnpqstvzɉḋḍŧṭṣñṇṅŋꝁǥꞓƀśʰ])'

    # Karakter ZWNJ
    zwnj = '\u200C'

    # Konsonan yang dikecualikan dari penyisipan ZWNJ
    pengecualian = {'y', 'w', 'r'} #, 'r', 'ṛ', 'ṝ', 'ḷ', 'ḹ'

    # Fungsi pengganti
    def replace_consonants(match):
        c1, c2, c3 = match.group(1), match.group(2), match.group(3)
        #if c1 in pengecualian or c3 in pengecualian:
        #    return f"{c1}{c2}{c3}"
        #if c1 == 's' and c2 == 't'and c3 == 'r':
        #    return f"{c1}{c2}{c3}"
        return f"{c1}{zwnj}{c2}{c3}"

    # Lakukan substitusi pada teks
    return re.sub(pattern, replace_consonants, text)
    
#Daftar sandi vokal
vowel_merge_rules_with_space = [
    # hanya untuk kasus vokal dengan spasi antaranya
    ('a', 'aw', ['u', 'i']),
    ('i', 'y',  ['a', 'u']),
    ('u', 'w',  ['a', 'i']),
    ('o', 'w',  ['a', 'i']),
    ('è', 'èy', ['ĕ']),
    ('ꜽ', 'ꜽy', ['a', 'u', 'è', 'ĕ', 'e', 'o', 'ā', 'ū', 'ē', 'ō']),
    ('ṙ', 'r',  ['a', 'ā', 'i', 'ī', 'u', 'ū', 'è', 'e', 'ĕ', 'o', 'ö', 'ꜽ', 'ꜷ']),
    # dst, sesuai kebutuhan
]
vowel_merge_rules_no_space = [
    # hanya untuk kasus vokal langsung berdampingan
    ('a', 'aw', ['u', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('i', 'y',  ['a', 'u', 'è', 'ĕ', 'e', 'o', 'ā', 'ū']),
    ('u', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('o', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('ꜷ', 'ꜷw', ['a', 'i', 'è', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('è', 'èy',  ['a', 'i', 'u', 'o']),
    ('è', 'èw', ['ū','o','u']),
]
vowel_merge_rules = [
    # kasus vokal langsung berdampingan atau tidak
    ('a', 'aw', ['u', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('i', 'y',  ['a', 'u', 'è', 'ĕ', 'e', 'o', 'ā', 'ū']),
    ('u', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('ū', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('o', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('ꜷ', 'ꜷw', ['a', 'i', 'è', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('ꜽ', 'ꜽy', ['a', 'u', 'è', 'ĕ', 'e', 'o', 'ā', 'ū', 'ē', 'ō']),
    ('è', 'èy',  ['a', 'i', 'u', 'o']),
    ('è', 'èw', ['ū','o','u']),
]

#hukum pertemuan vokal
def apply_vowel_merges_with_space(text, rules):
    for prefix, output_prefix, vowels in rules:
        for v in vowels:
            pattern = rf'{re.escape(prefix)}[^\S\n]+{re.escape(v)}' #dengan spasi
            replacement = f'{output_prefix}{v}'
            text = re.sub(pattern, replacement, text)
    return text
def apply_vowel_merges_no_space(text, rules):
    for prefix, output_prefix, vowels in rules:
        for v in vowels:
            pattern = rf'{re.escape(prefix)}{re.escape(v)}' #non spasi
            replacement = f'{output_prefix}{v}'
            text = re.sub(pattern, replacement, text)
    return text
def apply_vowel_merges(text, rules):
    for prefix, output_prefix, vowels in rules:
        for v in vowels:
            pattern = rf'{re.escape(prefix)}[^\S\n]*{re.escape(v)}' #non spasi
            replacement = f'{output_prefix}{v}'
            text = re.sub(pattern, replacement, text)
    return text

#tambahkan h pada pertemuan vokal yang tidak masuk hukum sandi
def insert_h_between_unmerged_vowels(text):
    vowels = 'aāiīuūèéĕeëoöōŏꜽꜷ'
    pattern = rf'([{vowels}])[^\S\n]*([{vowels}])'
    def repl(match):
        v1, v2 = match.group(1), match.group(2)
        # Jangan ubah jika sudah diubah oleh aturan vowel_merge_rules
        # Cek apakah kombinasi ini pernah ditangani
        for ruleset in (vowel_merge_rules_with_space, vowel_merge_rules_no_space, vowel_merge_rules):
            for prefix, _, allowed in ruleset:
                if v1 == prefix and v2 in allowed:
                    return match.group(0)  # Sudah ditangani, jangan ubah
        return f'{v1}h{v2}'
    return re.sub(pattern, repl, text)

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

def inisialisasi(text):
    DAFTAR_VOKAL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûôAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
    NON_HURUF_PENDAHULU = r'([^\w\s-])(\s*)'
    VOKAL_REGEX = f"[{DAFTAR_VOKAL}]"

    (re.compile(rf'^([{DAFTAR_VOKAL}])', re.MULTILINE), lambda m: {'ꜽ': 'Ꜽ', 'è': 'È', 'é': 'É'}.get(m.group(1), m.group(1).upper())), #Kapitalkan vokal di awal baris
    (re.compile(rf'{NON_HURUF_PENDAHULU}({VOKAL_REGEX})'), lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).upper()}"), #Kapitalkan vokal jika didahului tanda baca non-huruf (bukan spasi/strip)

    return text

def hukum_sandi(text):
    #Aksara suci
    DAFTAR_VOKAL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûôAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
    VOKAL_REGEX = f"[{DAFTAR_VOKAL}]" 
    text = re.sub(rf'\b({VOKAL_REGEX})(m|ṃ)\b', lambda m: f" \u200C{m.group(1).upper()}{m.group(2)}\u200C ", text)

    #pertahankan le
    DAFTAR_KONSONAN = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳkʰ"
    text = re.sub(rf'(?<=([{DAFTAR_KONSONAN}]))(ḷ|ḹ)',lambda m: m.group(2) + '\u200D',text)
    #hapus strip depan konsonan agar tidak menjadi kata baru
    text = re.sub(rf'-([{DAFTAR_KONSONAN}])',r'\1',text)
    
    # Hapus strip di tahap ini
    text = text.replace("-", " ")

    #agar aksara swara tidak dijadikan pasangan
    vokal_spesial = "AĀÂIĪÎUŪÛOŌÔEĔÊÉÈꜼꜶ"
    text = re.sub(rf"(?<=[{DAFTAR_KONSONAN.replace('ṙ','')}])[^\S\n]*([{vokal_spesial}])", lambda m: '\u200C' + m.group(1), text)

    # Regex penyeragaman vokal
    text = re.sub('|'.join(re.escape(k) for k in penyeragaman_vokal.keys()), 
                lambda match: penyeragaman_vokal[match.group(0)], text)

    #cegah ya dipasangi
    pengecualian_ya = set('aāiīuūeèoōöŏĕꜷꜽlwyr')
    text = re.sub(
    r'([yw])([^\S\n]+|-)(?=([^\s]))',
    lambda m: (m.group(1) + m.group(2) + ('' if m.group(3).lower() in pengecualian_ya else '\u200C')),text)

    identik = [('a', 'ā'), ('i', 'ī'), ('u', 'ū'), ('e', 'ꜽ'), ('o', 'ꜷ')]
    for base, long_form in identik:   
        # Gabungan vokal identik kecil → vokal panjang
        text = re.sub(rf'{base}[^\S\n]*{base}', long_form, text)
        text = re.sub(rf'{long_form}[^\S\n]*{long_form}', long_form, text)

    # Kombinasi sandhi vokal yang disederhanakan
    text = re.sub(r'[aā][^\S\n]+[iī]', 'e', text)   # a atau ā + i atau ī menjadi e
    text = re.sub(r'[aā][^\S\n]+[uū]', 'o', text)   # a atau ā + u atau ū menjadi o

    text = re.sub(r'ꜽ[^\S\n]*ꜽ', 'ꜽ', text)
    text = re.sub(r'ꜷ[^\S\n]*ꜷ', 'ꜷ', text)

    text = apply_vowel_merges_with_space(text, vowel_merge_rules_with_space)
    text = apply_vowel_merges_no_space(text, vowel_merge_rules_no_space)
    text = apply_vowel_merges(text, vowel_merge_rules)
    #text = insert_h_between_unmerged_vowels(text)
    
    # Untuk beberapa kasus khusus
    vokal = "aiuĕāâîīûūêôeèéöoꜽꜷ"
    text = re.sub(rf'ḥ[^\S\n]+([{vokal}])', lambda m: f"h{m.group(1).lower()}", text)
    text = re.sub(rf'ŋ[^\S\n]+([{vokal}])', lambda m: f"ṅ{m.group(1).lower()}", text)
    text = re.sub(rf'ṙ[^\S\n]+([{vokal}])', lambda m: f"r{m.group(1).lower()}", text)

    #Menyambung vokal dan konsonan yang terpisah spasi
    text = re.sub(r'([bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳkʰ])[^\S\n]*([aiuĕāâîīûūêôeèéöoꜽꜷ])', r'\1\2', text)

    return text

def hukum_penulisan(text):

    SUBSTITUTION_REGEX = [
    (re.compile(r'(?<=\s)ṙyy|^ṙyy', flags=re.MULTILINE), '\u200cꦪꦾꦂ'),
    (re.compile(r'akhir'), 'ꦄꦏ꦳ꦶꦂ'),
    (re.compile(r'\brŧ'), '\u200Cꦡꦂ'),
    #substitusi sigeg + zwnj
    (re.compile(r'ṅ‌'), 'ŋ')
    ]
    for pattern, replacement in SUBSTITUTION_REGEX:
        text = pattern.sub(replacement, text)

    daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳŋḥṙʰ"
    #tambah zwnj depan kata
    patterns = [
    r'\bhy',
    rf'\b([{daftar_konsonan}])(r|ṛ|ḷ|ṝ|ḹ|w|l)',
    #rf'\b([{daftar_konsonan.replace("p", "")}])(r|ṛ|ḷ|ṝ|ḹ|w|l)'
    r'\b(ḷ|ḹ)',    
    r'\b(w|ṅ)',
    r'lwi(r|ṙ)', 
    r'\byan\b', r'\bya\b', r'\bta(?:n|ṅ|ŋ)?\b',
    r"\bṅ(-)?(" + f"[{daftar_konsonan}]" + r")",  
    r'\bstr', r'\brkw', r'\bri', r'\bdwa\b',  
    ]
    text = add_zwnj_awal_kata_bulk(text, patterns, '\u200C', daftar_konsonan) 

    #cegah pasangan lebih dari tumpuk tiga
    text = insert_zwnj_between_consonants(text)

    #kasus sigeg-sigeg
    text = re.sub(r'ṙ[^\S\n]*ŋ', r'ṙṅ', text)
    text = re.sub(r'ḥ[^\S\n]*ŋ', r'ḥṅ', text)

    # Gabungkan ZWNJ dan ZWJ yang berulang menjadi satu saja
    text = re.sub(r'([\u200C\u200D])[\u200C\u200D]+', r'\1', text)
    text = re.sub(r'^[\u200C\u200D]+', '', text, flags=re.MULTILINE)

    return(text)

def finalisasi(hasil):   

    # Langkah 1: Lakukan regexp untuk spasi di sekitar metrum
    hasil = re.sub(r'[^\S\r\n]*([|–⏑⏓])[^\S\r\n]*', r' \1 ', hasil)
    hasil = re.sub(r'[^\S\r\n]{2,}', ' ', hasil)
    
    # Langkah 2: Panggil fungsi ganti_tanda_metrum
    hasil = ganti_tanda_metrum(hasil)

    penggantian = {
        # Pasangan la pepet dan la utuh
        '꧀ꦊ':'꧀ꦭꦼ',
       '꧀ꦭꦼ\u200D' : '꧀ꦊ',
        
        # Penggantian karakter dan simbol
        '꧀ꦪ': 'ꦾ',
        '꧀ꦫ': 'ꦿ',
        'ꦈꦴꦁ': 'ꦈꦴꦀ',
        '꧀ꦗ꧀ꦚ': '꧀\u200Dꦗ꧀ꦚ',
        'ꦫ꧀ꦮ': 'ꦫ꧀ꦮ\u200D',
        'ꦉꦴ': 'ꦉ\u200Cꦴ',
        '⏒꧇': '⏒ ꧇',
        ' ' : '', # Hapus spasi
        
        # Ganti simbol metrum
        '–': '‐',
        '⏑': '0',
        '⏓': '0̲',
        '=': ' = ',
        '❌': ' ❌',
        
        # Hapus karakter spasi dan tab
        '\t': ' ',
        '_': ' ',
    }

    # Langkah 3: Lakukan penggantian sederhana dalam satu iterasi
    for cari, ganti in penggantian.items():
        hasil = hasil.replace(cari, ganti)

    hasil = re.sub(r"=[^\S\n]+=[^\S\n]*", '==', hasil)
    
    return hasil