import re
from modul_jtwk.konstanta import VOKAL_NON_KAPITAL, DAFTAR_VOKAL, ZWNJ, DAFTAR_KONSONAN


def mode_normal(text):

    #Bahasa Indonesia
    #rf'([{DAFTAR_VOKAL}])([{DAFTAR_KONSONAN}])lah\b': r'\1\2 laḥ',  

    return text


def mode_kakawin(text):
    #Mode kakawin adalah transliterasi yang memaksa semua huruf vokal jadi kecil, pengkapitalan akan dilakukan oleh algoritma metrum

    #paksa  kapital swara jadi huruf kecil semua
    #text = text.lower()
    #Bahasa kawi tidak kenal ṙṇṇ
    text = re.sub(r'rṇ', 'rn', text) # khusus bahasa jawa kuno

    return text

def mode_lampah(text):

    return text

def mode_sriwedari(text):
    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    text = re.sub(rf"([{VOKAL_NON_KAPITAL}])([{VOKAL_NON_KAPITAL}])", r"\1ʰ\2",
             re.sub(rf"(\s)([{VOKAL_NON_KAPITAL}])", r"\1ʰ\2", text))
    
    text = re.sub(r'-', '', text, flags=re.IGNORECASE)

    # Regex untuk mengganti "ṅṅ" dengan "ŋŋ" sambil mempertahankan vokal
    text = re.sub(rf'(ṅṅ)([{VOKAL_NON_KAPITAL}])\b', r'ŋṅ\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'(hh)([{VOKAL_NON_KAPITAL}])\b', r'ḥh\2', text, flags=re.IGNORECASE)

    #text = re.sub(rf'\b(ṅg)([{VOKAL_NON_KAPITAL}])', r'haṅg\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'\b(ñj)([{VOKAL_NON_KAPITAL}])', r'hañj\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'wong', r'wwong', text, flags=re.IGNORECASE)
    return text

def mode_cerita(text):

    text = re.sub(r'-', '', text, flags=re.IGNORECASE)

    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    # Regex untuk mengganti "ṅṅ" dengan "ŋŋ" sambil mempertahankan vokal
    #text = re.sub(rf'(ṅṅ)([{VOKAL_NON_KAPITAL}])\b', r'ŋṅ\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'(hh)([{VOKAL_NON_KAPITAL}])\b', r'ḥh\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'\b(ṅg)([{VOKAL_NON_KAPITAL}])', r'haṅg\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'\b(ñj)([{VOKAL_NON_KAPITAL}])', r'hañj\2', text, flags=re.IGNORECASE)

    text = re.sub(r'(?<=\b)Ana(?=\b)', 'ʰana', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Iki(?=\b)', 'ʰiki', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Iku(?=\b)', 'ʰiku', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Udan(?=\b)', 'ʰudan', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Ambèk(?=\b)', 'ʰambèk', text, flags=re.IGNORECASE)

    return text

def mode_sanskrit(text):

    def ZWNJ_and_capitalize(match):
        spasi, vokal = match.groups()
        return spasi + ZWNJ + vokal.upper()

    text = re.sub(rf'(\s)([{DAFTAR_VOKAL.lower()}])', ZWNJ_and_capitalize, text)

    return text

def mode_satya(text):

    # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf dan spasi
    text = re.sub(rf'([^\w\s])(\s)([{VOKAL_NON_KAPITAL}])', lambda m: m.group(1) + m.group(2) + m.group(3).upper(), text)

    # Mengubah vokal menjadi uppercase jika didahului oleh spasi dan vokal, tanpa menghapus spasi tersebut
    text = re.sub(rf'(?<=o)([^\S\n]+)([{VOKAL_NON_KAPITAL}])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Aturan baru: menambahkan '/' sebelum spasi jika diapit oleh konsonan di kiri dan vokal uppercase di kanan
    #text = re.sub(r'([{DAFTAR_KONSONAN}])\s([AIUĀĪŪEOÖŎĔÈ])', r'\1\u200D \2', text)
    
    #khusus kakawin, urai vokal kapital yang didahuli spasi+konsonan
    text = re.sub(r"(?<=[DAFTAR_KONSONAN][DAFTAR_KONSONAN]) (A|I|U)", 
                lambda m: {'A': 'ā', 'I': 'ī', 'U': 'ū'}[m.group(1)], 
                text)
    #Perubahan pada rṇn
    text = re.sub(r'rṇ', 'rn', text, flags=re.IGNORECASE)

    return text