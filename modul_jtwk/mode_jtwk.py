import re

# Definisi variabel global
daftar_vokal = "ꜷꜽaāiīuūeèoōöŏĕ"  # Daftar vokal
vokal_lampah_spesial = "AIU"
vokal_kapital = "AĀIĪUŪEÈOŌÖŎĔꜶꜼ"  # Daftar vokal kapital
vokal_gabungan = "aāiīuūeèoōöŏĕꜷꜽAĀIĪUŪEÈOŌÖŎĔꜶꜼ"
daftar_konsonan = "bdfhjnptvwyzḋḍŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"  # Daftar konsonan
daftar_konsonan_sigeg = "ŋḥṃṙ"  # Daftar konsonan
zwnj = '\u200C'  # Zero-width non-joiner (ZWNJ)

def add_h_between_vowels(text):
    # Pola untuk mencocokkan vokal yang didahului oleh karakter selain huruf atau di awal kata
    pattern_non_letter = rf"(^|[^a-zA-Zḋḍŧṭṣñṇṅŋṛṝḷḹꝁǥꞓƀśyḳ-])([{daftar_vokal}])"

    # Pola untuk mencocokkan vokal yang berturut-turut di dalam kata
    pattern_consecutive_vowels = rf"([{daftar_vokal}])([{daftar_vokal}])"

    # Fungsi untuk menyisipkan 'h' sebelum vokal jika perlu
    def insert_h(match):
        sebelum_vokal = match.group(1)  # Karakter sebelum vokal
        vokal = match.group(2)  # Vokal yang ditemukan
        
        # Tambahkan 'h' sebelum vokal
        return sebelum_vokal + 'ʰ' + vokal

    # Fungsi untuk menyisipkan 'h' di antara dua vokal berturut-turut
    def insert_h_between_vowels(match):
        vokal_pertama = match.group(1)  # Vokal pertama
        vokal_kedua = match.group(2)    # Vokal kedua
        
        # Tambahkan 'h' di antara kedua vokal
        return vokal_pertama + 'ʰ' + vokal_kedua

    # Terapkan substitusi untuk pola yang mencocokkan vokal yang didahului oleh karakter non-huruf
    text = re.sub(pattern_non_letter, insert_h, text)

    # Terapkan substitusi untuk pola yang mencocokkan vokal berturut-turut di dalam kata
    return re.sub(pattern_consecutive_vowels, insert_h_between_vowels, text)

def mode_normal(text):

    # Mengubah vokal menjadi uppercase jika didahului oleh spasi dan vokal, tanpa menghapus spasi tersebut
    text = re.sub(rf'(?<=\b[{daftar_vokal}])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)
    # Mengubah vokal pertama setelah spasi menjadi uppercase jika didahului oleh spasi
    text = re.sub(rf'(?<=\s)([{daftar_vokal}])', lambda m: m.group(1).upper(), text)
    # Menghapus spasi sebelum vokal jika didahului oleh konsonan
    text = re.sub(rf'(?<=[^{daftar_vokal}])\s([{daftar_vokal}])', r'\1', text)

    text = re.sub(r'-', '', text, flags=re.IGNORECASE)
    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    text = add_h_between_vowels(text)

    # Inserting ZWNJ after the consonant if followed by space and capital vowel
    text = re.sub(rf'([{daftar_konsonan}])(\s)([{vokal_kapital}])', r'\1' + zwnj + r'\2\3', text)

    # Aturan baru: menambahkan '\u200C' sebelum spasi jika diapit oleh konsonan di kiri dan vokal uppercase di kanan
    text = re.sub(rf'([{daftar_konsonan}])\s([AIUĀĪŪEOÖŎĔÈ])', lambda m: m.group(1) + '\u200C' + ' ' + m.group(2), text)

    return text

def mode_modern_lampah(text):
    #Menambahkan a didepan untuk ater2 anuswara cth nduwe=anduwe
    text = re.sub(r'\b(n)([bcdfghjklmnpqrstvwxyz])(?=\w*)', r'a\1\2', text)

    # Mengubah vokal menjadi uppercase jika didahului oleh spasi dan vokal, tanpa menghapus spasi tersebut
    text = re.sub(rf'(?<=\b[{daftar_vokal}])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)
    # Mengubah vokal pertama setelah spasi menjadi uppercase jika didahului oleh spasi
    text = re.sub(rf'(?<=\s)([{daftar_vokal}])', lambda m: m.group(1).upper(), text)
    # Menghapus spasi sebelum vokal jika didahului oleh konsonan
    text = re.sub(rf'(?<=[^{daftar_vokal}])\s([{daftar_vokal}])', r'\1', text)

    text = re.sub(r'-', '', text, flags=re.IGNORECASE)
    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    text = add_h_between_vowels(text)

    # Inserting ZWNJ after the consonant if followed by space and capital vowel
    text = re.sub(rf'([{daftar_konsonan}])(\s)([{vokal_kapital}])', r'\1' + zwnj + r'\2\3', text)

    return (text)

def mode_kakawin(text):

    # Menyisipkan ZWNJ dan mengkapitalkan vokal jika didahului tanda baca non-huruf (bukan spasi/strip)
    '''
    text = re.sub(
        rf'([^\w\s-])(\s*)([{daftar_vokal}])',
        lambda m: f"{m.group(1)}{m.group(2)}{zwnj}{m.group(3).upper()}",
        text
    )
    '''
    #Perubahan pada rṇn
    #text = re.sub(r'rṇ', 'rn', text, flags=re.IGNORECASE)
    # 
    #text = re.sub(r'i[^\S\n]+a', 'i ha', text)
    
    text = re.sub(r'rṇ', 'rn', text) # khusus bahasa jawa kuno

    return text

def mode_lampah(text):

    # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf dan spasi
    text = re.sub(rf'([^\w\s])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2) + m.group(3).upper(), text)

    # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf
    text = re.sub(rf'([^\w\s])([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Kapitalkan vokal di awal baris
    text = re.sub(rf'(^|\n)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Aturan baru: menambahkan '/' sebelum spasi jika diapit oleh konsonan di kiri dan vokal uppercase di kanan
    text = re.sub(r'([{daftar_konsonan}])\s([AIUĀĪŪEOÖŎĔÈ])', r'\1\ \2', text)
    
    #khusus kakawin, urai vokal kapital yang didahuli spasi+konsonan
    text = re.sub(r"(?<=[daftar_konsonan][daftar_konsonan]) (A|I|U)", 
                lambda m: {'A': 'ā', 'I': 'ī', 'U': 'ū'}[m.group(1)], 
                text)


    return text


##def mode_lampah(text):
'''
    #kapitalkan dan berikan zwnj jika bertemu huruf ini
    text = re.sub(r"([AĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ])", r"\u200C\1", text); print(text)

    # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf dan spasi
    text = re.sub(rf'([^\w\s])(\s)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2) + m.group(3).upper(), text)

    # Mengubah vokal menjadi uppercase jika didahului oleh tanda baca non-huruf
    text = re.sub(rf'([^\w\s])([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Kapitalkan vokal di awal baris
    text = re.sub(rf'(^|\n)([{daftar_vokal}])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Aturan baru: menambahkan '/' sebelum spasi jika diapit oleh konsonan di kiri dan vokal uppercase di kanan
    text = re.sub(r'([{daftar_konsonan}])\s([AIUĀĪŪEOÖŎĔÈ])', r'\1/ \2', text)
    
    #khusus kakawin, urai vokal kapital yang didahuli spasi+konsonan
    text = re.sub(r"(?<=[daftar_konsonan][daftar_konsonan]) (A|I|U)", 
                lambda m: {'A': 'ā', 'I': 'ī', 'U': 'ū'}[m.group(1)], 
                text)

    

    return text
'''

def mode_sriwedari(text):
    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    text = add_h_between_vowels(text)
    text = re.sub(r'-', '', text, flags=re.IGNORECASE)
    # Regex untuk mengganti "ṅṅ" dengan "ŋŋ" sambil mempertahankan vokal
    text = re.sub(rf'(ṅṅ)([{daftar_vokal}])\b', r'ŋṅ\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'(hh)([{daftar_vokal}])\b', r'ḥh\2', text, flags=re.IGNORECASE)
    #text = re.sub(rf'\b(ṅg)([{daftar_vokal}])', r'haṅg\2', text, flags=re.IGNORECASE)
    text = re.sub(rf'\b(ñj)([{daftar_vokal}])', r'hañj\2', text, flags=re.IGNORECASE)
    return text

def mode_cerita(text):

    text = re.sub(r'-', '', text, flags=re.IGNORECASE)

    # Fungsi untuk menambahkan 'h' di depan kata yang dimulai dengan vokal setelah spasi
    text = add_h_between_vowels(text)
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