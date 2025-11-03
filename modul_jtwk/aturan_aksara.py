#Menghapus spasi ada di aturan aksara
import re
from modul_jtwk.konstanta import VOKAL_KAPITAL, VOKAL_NON_KAPITAL, DAFTAR_VOKAL, DAFTAR_KONSONAN, ZWNJ, ZWSP, ZWJ, VOKAL_PANJANG

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
    **{huruf: 'ꦏ꦳꧀' for huruf in ('ḳ', 'Ḳ', 'q', 'Q')}
    #**{huruf: 'ꦏ꧀ꦰ꧀' for huruf in ('v', 'V')},
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
    **{tanda: 'ꦼ' for tanda in ('ĕ', 'ě')},
    **{tanda: 'ꦺꦴ' for tanda in ('o', 'ô')},
    **{tanda: 'ꦺ' for tanda in ('è', 'é', 'e', 'ê')},
    **{tanda: 'ꦀ' for tanda in ('ṃ', 'm̃', 'ᶆ', 'ṁ')},
    **{tanda: 'ꦁ' for tanda in ('ŋ', 'ᶇ')},
    **{tanda: 'ꦃ' for tanda in ('ḥ', 'ꞕ')},
    **{tanda: 'ꦂ' for tanda in ('ṙ', 'ᶉ')},
}

swara = {
    # Swara
    'A': 'ꦄ','I': 'ꦅ', 'U': 'ꦎ','O': 'ꦈ',
    'Ꜽ': 'ꦍ', 'Ö': 'ꦄꦼꦴ', 'Ĕ': 'ꦄꦼ',

    **{bunyi: 'ꦄꦴ' for bunyi in ('Ā', 'Â')},
    **{bunyi: 'ꦇ' for bunyi in ('Ī', 'Î')},
    **{bunyi: 'ꦎꦴ' for bunyi in ('Ū', 'Û')},
    **{bunyi: 'ꦌ' for bunyi in ('E', 'È','É')},
    **{bunyi: 'ꦄꦼ' for bunyi in ('Ĕ')},
    **{bunyi: 'ꦈꦴ' for bunyi in ('Ŏ', 'Ō', 'Ꜷ')},
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
    '%' : f'{ZWSP}꧄‍꧉ꦧ꧀ꦖ꧉꧄‍{ZWSP}', '^' : f'{ZWSP}꧄‍꧉ꦟ꧀ꦢꦿ꧉꧄‍{ZWSP}', '&' : f'{ZWSP}꧄‍꧉ꦅ꧉꧄‍{ZWSP}'
}

PENYERAGAMAN_VOKAL = {}
for kunci, nilai in [
    (['â'], 'ā'),
    (['î'], 'ī'),
    (['ô'], 'o'),
    (['ê', 'é', 'è'], 'e'),
    (['û'], 'ū'),
    (['ē','~'], ''),
    (['lĕ', 'ḷĕ', 'l̥'], 'ḷ'),
    (['lö', 'ḹö', 'l̥̄'], 'ḹ'),
    (['rĕ', 'ṛĕ', 'r̥'], 'ṛ'),
    (['rö', 'ṝö', 'r̥̄'], 'ṝ'),
]:
    PENYERAGAMAN_VOKAL.update(dict.fromkeys(kunci, nilai))

VOWEL_MERGE_RULES_WITH_SPACE = [
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

VOWEL_MERGE_RULES_NO_SPACE = [
    # hanya untuk kasus vokal langsung berdampingan
    ('a', 'aw', ['u', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('i', 'y',  ['a', 'u', 'è', 'ĕ', 'e', 'o', 'ā', 'ū']),
    ('u', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('o', 'w',  ['a', 'i', 'è', 'é', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('ꜷ', 'ꜷw', ['a', 'i', 'è', 'ĕ', 'e', 'o', 'ā', 'ī', 'ō', 'ŏ']),
    ('è', 'èy',  ['a', 'i', 'u', 'o']),
    ('è', 'èw', ['ū','o','u']),
]

VOWEL_MERGE_RULES = [
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

def ganti_tanda_metrum(hasil):
    def ganti_tanda(match):
        baris = match.group()
        baris = re.sub(r'꧋[\u200C\u200D]*', '[', baris)
        baris = re.sub(r'꧊[\u200C\u200D]*', ']', baris)
        return baris

    hasil = re.sub(r'^.*[—⏑⏓].*꧋[\u200C\u200D]*.*$', ganti_tanda, hasil, flags=re.MULTILINE)
    hasil = re.sub(r'^.*[—⏑⏓].*꧊[\u200C\u200D]*.*$', ganti_tanda, hasil, flags=re.MULTILINE)
    hasil = hasil.replace("]×","] × ")
    return hasil

def insert_zwnj_between_consonants(text):
    # Pola pencocokan: konsonan + spasi + konsonan + konsonan
    pattern = r'([bcdfghjklmnpqstvzɉḋḍŧṭṣñṇṅꝁǥꞓƀśʰ])[^\S\n]*([ybcdfghjklmnqtvwzɉḋḍŧṭñṇṅꝁǥꞓƀśʰ])[^\S\n]*([ḷḹbcdfghjklmnpqstvzɉḋḍŧṭṣñṇṅꝁǥꞓƀśʰ])'

    # Konsonan yang dikecualikan dari penyisipan ZWNJ
    # pengecualian = {'y', 'w', 'r'} #, 'r', 'ṛ', 'ṝ', 'ḷ', 'ḹ'

    # Fungsi pengganti
    def replace_consonants(match):
        c1, c2, c3 = match.group(1), match.group(2), match.group(3)
        #if c1 in pengecualian or c3 in pengecualian:
        #    return f"{c1}{c2}{c3}"
        #if c1 == 's' and c2 == 't'and c3 == 'r':
        #    return f"{c1}{c2}{c3}"
        return f"{c1}{ZWNJ}{c2}{c3}"

    # Lakukan substitusi pada teks
    return re.sub(pattern, replace_consonants, text)

#Daftar sandi vokal
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
    pattern = rf'([{DAFTAR_VOKAL}])[^\S\n]*([{DAFTAR_VOKAL}])'
    def repl(match):
        v1, v2 = match.group(1), match.group(2)
        # Jangan ubah jika sudah diubah oleh aturan VOWEL_MERGE_RULES
        # Cek apakah kombinasi ini pernah ditangani
        for ruleset in (VOWEL_MERGE_RULES_WITH_SPACE, VOWEL_MERGE_RULES_NO_SPACE, VOWEL_MERGE_RULES):
            for prefix, _, allowed in ruleset:
                if v1 == prefix and v2 in allowed:
                    return match.group(0)  # Sudah ditangani, jangan ubah
        return f'{v1}h{v2}'
    return re.sub(pattern, repl, text)

RE_INISIALISASI_AKSARA = [
    # Ganti * ujung pupuh
    (re.compile(r'\*(\s*[#\<{])'), r'#\1'),
    # Kapitalkan vokal di awal baris
    (re.compile(rf'^([{DAFTAR_VOKAL}])', re.MULTILINE), 
        lambda m: {'ꜽ': 'Ꜽ', 'è': 'È', 'é': 'É'}.get(m.group(1), m.group(1).upper())),
    # Kapitalkan vokal jika didahului tanda baca non-huruf    
    (re.compile(rf'([^\w\s-])(\s*)([{DAFTAR_VOKAL}])'),
        lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).upper()}"),
]

def inisialisasi_aksara(text):
    for regex, repl in RE_INISIALISASI_AKSARA: text = regex.sub(repl, text)

    return text


RE_HUKUM_SANDI = [
    # aksara suci (m-ending)
    (re.compile(rf'\b([{DAFTAR_VOKAL}])(m|ṃ)\b'), 
        lambda m: f" {ZWNJ}{m.group(1).upper()}{m.group(2)}{ZWNJ} "),
    # pertahankan le
    (re.compile(rf'(?<=([{DAFTAR_KONSONAN}]))(ḷ|ḹ)'), lambda m: m.group(2) + '\u200D'),
    # hapus strip depan konsonan
    (re.compile(rf'-([{DAFTAR_KONSONAN}])'), r' \1'),
    # agar aksara swara tidak jadi pasangan
    (re.compile(rf"(?<=[{DAFTAR_KONSONAN.replace('ṙ','')}])[^\S\n]*([{VOKAL_KAPITAL}])"),
        lambda m: ZWNJ + m.group(1)),
    # kasus tabrakan font bagian taling
    #(re.compile(rf'ṙ([{DAFTAR_KONSONAN}])([{DAFTAR_KONSONAN}])([{DAFTAR_VOKAL}])(\s*)([{DAFTAR_KONSONAN}]+)(e|o)'), rf'ṙ\1\2\3{ZWNJ}\4\5\6'),
    (re.compile(rf'ṙ([{DAFTAR_KONSONAN.replace('ṙ','').replace('ŋ','').replace('ḥ','')}]{{2,}})([{DAFTAR_VOKAL}])(\s*)([{DAFTAR_KONSONAN}])(e|o)'), rf'ṙ\1\2{ZWNJ}\3\4\5'),

]

def hukum_sandi(text):
    for regex, repl in RE_HUKUM_SANDI: text = regex.sub(repl, text)

    text = text.replace("-", " ")
    text = re.sub('|'.join(map(re.escape, PENYERAGAMAN_VOKAL)), lambda m: PENYERAGAMAN_VOKAL[m.group(0)], text)

    #cegah ya dipasangi
    pengecualian_ya = set(VOKAL_NON_KAPITAL + 'wyrṛṝl')
    text = re.sub(r'([y])([^\S\n]*|-)(?=([^\s]))',
        lambda m: m.group(1)+m.group(2)+('' if m.group(3).lower() in pengecualian_ya else ZWNJ), text)

    # vokal identik dan sandhi
    for base,long_form in [('a','ā'),('i','ī'),('u','ū'),('e','ꜽ'),('o','ꜷ')]:
        text = re.sub(rf'{base}[^\S\n]*{base}', long_form, text)
        text = re.sub(rf'{long_form}[^\S\n]*{long_form}', long_form, text)
    text = re.sub(r'[aā][^\S\n]+[iī]', 'e', text)
    text = re.sub(r'[aā][^\S\n]+[uū]', 'o', text)
    text = re.sub(r'ꜽ[^\S\n]*ꜽ', 'ꜽ', text)
    text = re.sub(r'ꜷ[^\S\n]*ꜷ', 'ꜷ', text)

    # merge antar vokal
    text = apply_vowel_merges_with_space(text, VOWEL_MERGE_RULES_WITH_SPACE)
    text = apply_vowel_merges_no_space(text, VOWEL_MERGE_RULES_NO_SPACE)
    text = apply_vowel_merges(text, VOWEL_MERGE_RULES)
    return text


# Kompilasi substitusi utama
RE_HUKUM_PENULISAN = [
    # konsonan rangkap setelah perpisahan kata
    (re.compile(rf'([{DAFTAR_KONSONAN.replace("ḥ","").replace("ŋ","").replace("ṙ","").replace("ñ","").replace("ṇ","")}]\s+)([{"dwhgm"}][{DAFTAR_VOKAL}][{DAFTAR_KONSONAN}][{DAFTAR_KONSONAN}])'), rf'\1{ZWNJ}\2'),
    #konsonan rangkap setelah perpisahan kata versi sigeg
    (re.compile(rf'([{DAFTAR_KONSONAN.replace("ḥ","").replace("ŋ","").replace("ṙ","").replace("ñ","").replace("ṇ","")}]\s+)([{DAFTAR_KONSONAN}][{DAFTAR_VOKAL}][ṙḥŋ])'), rf'\1{ZWNJ}\2'),
    #perpisahan kata: dua suku kata akhiran suku kata panjang
    (re.compile(rf'(?<=[{DAFTAR_KONSONAN}]\s)([{DAFTAR_KONSONAN}][{DAFTAR_VOKAL}][{DAFTAR_KONSONAN}][{VOKAL_PANJANG}])'), rf'{ZWNJ}\1'),

    # sambung konsonan dan vokal terpisah spasi
    (re.compile(rf'([{DAFTAR_KONSONAN}])[^\S\n]*([{DAFTAR_VOKAL}])'), r'\1\2'),

]

SUBSTITUSI_SIGEG = [
    #Kasus ryy dan rth
    (re.compile(r'(?<=\s)ṙyy|^ṙyy', re.MULTILINE), f'{ZWNJ}ꦪꦾꦂ'),
    (re.compile(r'\brŧ'), f'{ZWNJ}ꦡꦂ'),

    #substitusi sigeg + zwnj
    (re.compile(r'ṅ‌'), 'ŋ'),
    #zwnj sebelum konsonan+vokal+ŋ
    (re.compile(rf'([{DAFTAR_KONSONAN.replace("ḥ","").replace("ŋ","").replace("ṙ","")}][^\S\n]+)([{DAFTAR_KONSONAN.replace("n","")}])([{DAFTAR_VOKAL}])ŋ'), rf'\1{ZWNJ}\2\3ŋ'),
]

def hukum_penulisan(text):
    for r, s in RE_HUKUM_PENULISAN + SUBSTITUSI_SIGEG: text = r.sub(s, text)

    # sisipkan ZWNJ antar pola
    def sisipkan_zwnj_pola(text, pola_list):
        for pola_x, pola_y in pola_list:
            text = re.sub(f"({pola_x})({pola_y})", rf"\1{ZWNJ}\2", text, flags=re.IGNORECASE)
        return text

    def buat_pola(h, targets): return [(rf"{h}\b ", t) for t in targets]

    konsonan_spasi = rf"[{DAFTAR_KONSONAN.replace('ḥ','').replace('ŋ','').replace('ṙ','').replace('ñ','').replace('ṇ','')}][^\S\n]+"
    pola_list = [
        *buat_pola("l", ["h","t"]), 
        *buat_pola("t", ["c","l","b","k","ḍ"]),
        *buat_pola("s", ["w","k","ḍ","n","s"]), 
        *buat_pola("k", ["l","w","p","ś","j"]),
        *buat_pola("n", ["ś","l","j","w"]), 
        *buat_pola("p", ["j","ś","g"]), 
        *buat_pola("m", ["g"]),
        (konsonan_spasi, r"(duḥk|duḥꝁ|jñ)"),
        (konsonan_spasi, rf"([{DAFTAR_KONSONAN.replace('p','').replace('s','')}])(r|ṛ|ḷ|ṝ|ḹ|w|l|y|w)"),
        (konsonan_spasi, r"(ḷ|ḹ|r|w|y|ǥ|ñ|ɉ|ṅ|h|l|lĕ|rĕ|lö|rö)"),
        (konsonan_spasi, r"(ṅ(-)?[" + DAFTAR_KONSONAN + r"])"),
        (konsonan_spasi, r"(str|sꝑ|sŧ)"),
        (konsonan_spasi, rf"([{DAFTAR_KONSONAN}][{VOKAL_PANJANG}])"),
        (konsonan_spasi, rf"([{DAFTAR_KONSONAN}][{DAFTAR_KONSONAN}])"),
    ]
    text = sisipkan_zwnj_pola(text, pola_list)
    return insert_zwnj_between_consonants(text)


def finalisasi(hasil):

    penggantian = {
        # Pasangan la pepet dan la utuh
        '꧀ꦊ':'꧀ꦭꦼ',
       f'꧀ꦭꦼ\u200D' : '꧀ꦊ',

        # Penggantian karakter dan simbol
        '꧀ꦪ': 'ꦾ',
        '꧀ꦫ': 'ꦿ',
        'ꦈꦴꦁ': 'ꦈꦴꦀ',
        '꧀ꦭꦼ': '꧀ꦭ‍ꦼ',
        #'ꦉꦴ': f'ꦉ{ZWNJ}ꦴ',
        '⏒꧇': '⏒ ꧇',
        '!': '',
        '_': f'{ZWNJ}',
        'ꦫ꧀ꦮ': f'ꦫ꧀ꦮ{ZWJ}',
        ' ' : '', # Hapus spasi

        # Ganti simbol metrum
        '⏑': '0',
        '⏓': '0̲',
        '=': ' = ',
        '❌': ' ❌',
        '`': f'{ZWNJ}',

        # Hapus karakter spasi dan tab
        '\t': ' ',
        #'_': ' ',
    }

    # Langkah 1: Lakukan penggantian sederhana dalam satu iterasi
    for cari, ganti in penggantian.items():
        hasil = hasil.replace(cari, ganti)

    # Pastikan 0̲ ditangani dulu
    #hasil = re.sub(r'[^\S\r\n]*(\||—|⏑|⏓|—)[^\S\r\n]*', r' \1 ', hasil)
    #hasil = re.sub(r'[^\S\r\n]{2,}', ' ', hasil)

    # Langkah 2: Panggil fungsi ganti_tanda_metrum
    hasil = ganti_tanda_metrum(hasil)

    #tanda sama dengan di lebih dari satu
    hasil = re.sub(r"=[^\S\n]+=[^\S\n]*", '==', hasil)

    # Hapus zwnj awal baris
    hasil = re.sub(r'^[ \u200C\u200D]+', '', hasil, flags=re.MULTILINE)

    # Gabungkan ZWNJ dan ZWJ yang berulang menjadi satu saja
    hasil = re.sub(r'[^\S\n]*[\u200C\u200D]{2,}', lambda m: m.group(0)[0], hasil, flags=re.MULTILINE)

    return hasil