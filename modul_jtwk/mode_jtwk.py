import re

# Definisi variabel global
daftar_vokal = "aiuĕāâîīûūêôeèéöoꜽꜷ"  # Daftar vokal
vokal_kapital = "AĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ"  # Daftar vokal kapital
vokal_gabungan = "aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ"
daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳʰ"  # Daftar konsonan
zwnj = '\u200C'  # Zero-width non-joiner (ZWNJ)

def mode_normal(text):

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
    text = re.sub(rf"([{daftar_vokal}])([{daftar_vokal}])", r"\1ʰ\2",
             re.sub(rf"(\s)([{daftar_vokal}])", r"\1ʰ\2", text))
    
    text = re.sub(r'-', '', text, flags=re.IGNORECASE)

    # Regex untuk mengganti "ṅṅ" dengan "ŋŋ" sambil mempertahankan vokal
    text = re.sub(rf'(ṅṅ)([{daftar_vokal}])\b', r'ŋṅ\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'(hh)([{daftar_vokal}])\b', r'ḥh\2', text, flags=re.IGNORECASE)

    #text = re.sub(rf'\b(ṅg)([{daftar_vokal}])', r'haṅg\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'\b(ñj)([{daftar_vokal}])', r'hañj\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'wong', r'wwong', text, flags=re.IGNORECASE)
    return text

def mode_cerita(text):

    text = re.sub(r'-', '', text, flags=re.IGNORECASE)

    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    # Regex untuk mengganti "ṅṅ" dengan "ŋŋ" sambil mempertahankan vokal
    #text = re.sub(rf'(ṅṅ)([{daftar_vokal}])\b', r'ŋṅ\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'(hh)([{daftar_vokal}])\b', r'ḥh\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'\b(ṅg)([{daftar_vokal}])', r'haṅg\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'\b(ñj)([{daftar_vokal}])', r'hañj\2', text, flags=re.IGNORECASE)

    text = re.sub(r'(?<=\b)Ana(?=\b)', 'ʰana', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Iki(?=\b)', 'ʰiki', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Iku(?=\b)', 'ʰiku', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Udan(?=\b)', 'ʰudan', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)Ambèk(?=\b)', 'ʰambèk', text, flags=re.IGNORECASE)

    return text

def mode_sanskrit(text):

    def zwnj_and_capitalize(match):
        spasi, vokal = match.groups()
        return spasi + zwnj + vokal.upper()

    text = re.sub(rf'(\s)([{vokal_gabungan.lower()}])', zwnj_and_capitalize, text)

    return text

def mode_satya(text):

    # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf dan spasi
    text = re.sub(rf'([^\w\s])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2) + m.group(3).upper(), text)

    # Mengubah vokal menjadi uppercase jika didahului oleh spasi dan vokal, tanpa menghapus spasi tersebut
    text = re.sub(rf'(?<=o)([^\S\n]+)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Aturan baru: menambahkan '/' sebelum spasi jika diapit oleh konsonan di kiri dan vokal uppercase di kanan
    #text = re.sub(r'([{daftar_konsonan}])\s([AIUĀĪŪEOÖŎĔÈ])', r'\1\u200D \2', text)
    
    #khusus kakawin, urai vokal kapital yang didahuli spasi+konsonan
    text = re.sub(r"(?<=[daftar_konsonan][daftar_konsonan]) (A|I|U)", 
                lambda m: {'A': 'ā', 'I': 'ī', 'U': 'ū'}[m.group(1)], 
                text)
    #Perubahan pada rṇn
    text = re.sub(r'rṇ', 'rn', text, flags=re.IGNORECASE)

    return text