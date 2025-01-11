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
    **{huruf: 'ꦯ꧀' for huruf in ('ś', 'Ś')},
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
    'ā': 'ꦴ',
    'ī': 'ꦷ',
    'ū': 'ꦹ',
    'ꜽ': 'ꦻ',
    'ꜷ': 'ꦻꦴ',
    'ö': 'ꦼꦴ',

    **{tanda: 'ꦼ' for tanda in ('e', 'ĕ')}, 
    **{tanda: 'ꦺꦴ' for tanda in ('o', 'ô')}, 
    **{tanda: 'ꦺ' for tanda in ('è', 'é')}, 
    **{tanda: 'ꦀ' for tanda in ('ṃ', 'ṃ', 'ᶆ')}, 
    **{tanda: 'ꦁ' for tanda in ('ŋ', 'ᶇ')}, 
    **{tanda: 'ꦃ' for tanda in ('ḥ', 'ꞕ')}, 
    **{tanda: 'ꦂ' for tanda in ('ṙ', 'ᶉ')},
}

swara = {
    # Swara
    'A': 'ꦄ', 'Ā': 'ꦄꦴ', 'I': 'ꦅ', 'Ī': 'ꦆ', 'U': 'ꦎ', 'Ū': 'ꦎꦴ', 'O': 'ꦈ',
    'Ꜷ': 'ꦈꦴ', 'Ꜽ': 'ꦍ', 'Ö': 'ꦄꦼꦴ', 'È': 'ꦌ',
    **{bunyi: 'ꦄꦼ' for bunyi in ('E', 'Ĕ')},
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
    '(': '꧌', ')': '꧍', '<': '꧁', '>': '꧂', ':': '꧇', '*': '꧄', 
}

def hukum_sandi(text):
    text = text.replace("/", "\u200C")
    text = text.replace("ô", "o")
    text = re.sub(r'akhir', 'ꦄꦏ꦳ꦶꦂ', text, flags=re.IGNORECASE)
    #Menyambung vokal partikel, catatan AĀIĪUŪEOÖŎĔꜸꜼ
    text = re.sub(r'([b-df-hj-np-tv-zḋḍŧṭṣñṇ])\s([aāiīuūeèoōöŏĕꜷꜽ])', r'\1\2', text)
  
    # Kombinasi vokal panjang
    text = re.sub(r'a\s+a', 'ā', text)
    text = re.sub(r'i\s+i', 'ī', text)
    text = re.sub(r'u\s+u', 'ū', text)

    text = re.sub(r'ā\s+ā', 'ā', text)
    text = re.sub(r'ī\s+ī', 'ī', text)
    text = re.sub(r'ū\s+ū', 'ū', text)

    # Kombinasi vokal identik
    text = re.sub(r'è\s+è', 'ꜽ', text)
    text = re.sub(r'o\s+o', 'ꜷ', text)

    # Kombinasi sandhi vokal yang disederhanakan
    text = re.sub(r'[aā]\s+[iī]', 'è', text)   # a atau ā + i atau ī menjadi e
    text = re.sub(r'[aā]\s+[uū]', 'o', text)   # a atau ā + u atau ū menjadi o

    text = re.sub(r'[iī]\s+[aā]', 'è', text)   # i atau ī + a atau ā menjadi e
    text = re.sub(r'[uū]\s+[aā]', 'o', text)   # u atau ū + a atau ā menjadi o

    # Aturan tambahan untuk vokal panjang yang bertemu dengan dirinya sendiri (tidak ada perubahan)
    text = re.sub(r'ꜽ\s+ꜽ', 'ꜽ', text)
    text = re.sub(r'ꜷ\s+ꜷ', 'ꜷ', text)

    #panglancar
    # Ganti kombinasi vokal 'u' dengan vokal lainnya
    text = re.sub(r'ua', 'wa', text)
    text = re.sub(r'ui', 'wi', text)
    text = re.sub(r'uè', 'wè', text)
    text = re.sub(r'uĕ', 'wĕ', text)
    text = re.sub(r'ue', 'we', text)
    text = re.sub(r'uo', 'wo', text)
    text = re.sub(r'uā', 'wā', text)
    text = re.sub(r'uī', 'wī', text)
    text = re.sub(r'uō', 'wō', text)
    text = re.sub(r'uŏ', 'wŏ', text)

    text = re.sub(r'ꜷa', 'ꜷwa', text)
    text = re.sub(r'ꜷi', 'ꜷwi', text)
    text = re.sub(r'ꜷè', 'ꜷwè', text)
    text = re.sub(r'ꜷĕ', 'ꜷwĕ', text)
    text = re.sub(r'ꜷe', 'ꜷwe', text)
    text = re.sub(r'ꜷo', 'ꜷwo', text)
    text = re.sub(r'ꜷā', 'ꜷwā', text)
    text = re.sub(r'ꜷī', 'ꜷwī', text)
    text = re.sub(r'ꜷō', 'ꜷwō', text)
    text = re.sub(r'ꜷŏ', 'ꜷwŏ', text)

    # Ganti kombinasi vokal 'i' dengan vokal lainnya
    text = re.sub(r'ia', 'ya', text)
    text = re.sub(r'iu', 'yu', text)
    text = re.sub(r'iè', 'yè', text)
    text = re.sub(r'iĕ', 'yĕ', text)
    text = re.sub(r'ie', 'ye', text)
    text = re.sub(r'io', 'yo', text)
    text = re.sub(r'ia', 'yā', text)
    text = re.sub(r'iu', 'yū', text)
    text = re.sub(r'ie', 'yē', text)
    text = re.sub(r'io', 'yō', text)

    text = re.sub(r'ꜽa', 'ꜽya', text)
    text = re.sub(r'ꜽu', 'ꜽyu', text)
    text = re.sub(r'ꜽè', 'ꜽyè', text)
    text = re.sub(r'ꜽĕ', 'ꜽyĕ', text)
    text = re.sub(r'ꜽe', 'ꜽye', text)
    text = re.sub(r'ꜽo', 'ꜽyo', text)
    text = re.sub(r'ꜽa', 'ꜽyā', text)
    text = re.sub(r'ꜽu', 'ꜽyū', text)
    text = re.sub(r'ꜽe', 'ꜽyē', text)
    text = re.sub(r'ꜽo', 'ꜽyō', text)

    #kasus layar/repha
    text = re.sub(r'ṙ\s+a', 'ra', text)
    text = re.sub(r'ṙ\s+ā', 'rā', text)
    text = re.sub(r'ṙ\s+i', 'ri', text)
    text = re.sub(r'ṙ\s+ī', 'rī', text)
    text = re.sub(r'ṙ\s+u', 'ru', text)
    text = re.sub(r'ṙ\s+ū', 'rū', text)
    text = re.sub(r'ṙ\s+è', 'rè', text)
    text = re.sub(r'ṙ\s+e', 're', text)
    text = re.sub(r'ṙ\s+ĕ', 'rĕ', text)
    text = re.sub(r'ṙ\s+o', 'ro', text)
    text = re.sub(r'ṙ\s+ö', 'rö', text)
    text = re.sub(r'ṙ\s+ꜽ', 'rꜽ', text)
    text = re.sub(r'ṙ\s+ꜷ', 'rꜷ', text)

    # List of lowercase vowels for case-sensitive matching
    lowercase_vowels = "aāiīuūeèoöŏĕꜷꜽ"

    # Update the patterns to match only lowercase vowels after 'ḥ' or 'ŋ'
    text = re.sub(rf'ḥ\s+([{lowercase_vowels}])', r'h\1', text)
    text = re.sub(rf'ŋ\s+([{lowercase_vowels}])', r'ṅ\1', text)

    return text

def finalisasi(hasil):
# Menghapus semua spasi setelah konversi
    hasil = hasil.replace(" ", "")
    hasil = hasil.replace("\t", " ")
    hasil = hasil.replace("~", " ")
    hasil = hasil.replace("_", " ")

    #ḷ untuk nga lelet, le untuk la pepet
    hasil = hasil.replace('ꦊꦼ', 'ꦊ')
    hasil = hasil.replace('ꦋꦼꦴ', 'ꦋ') 
    hasil = hasil.replace('‌꧀ꦭꦼ', ' ꧀ꦭꦼ') #tambahan
    hasil = hasil.replace('ꦭꦼ', 'ꦊ') #tambahan
    hasil = hasil.replace('‌ꦭꦼ', 'ꦊ') #zwnj+le untuk kasus unicode la pepet

    hasil = hasil.replace('ꦉꦼ', 'ꦉ')
    hasil = hasil.replace('ꦫꦼꦴ', 'ꦉꦴ')
    hasil = hasil.replace('ꦉꦴꦼꦴ', 'ꦉꦴ')
    hasil = hasil.replace('ꦿꦼꦴ', 'ꦽꦴ')
    hasil = hasil.replace('ꦿꦼ', 'ꦽ')
    hasil = hasil.replace('ꦽꦴꦼ', 'ꦽꦴ')
    hasil = hasil.replace('ꦽꦼ', 'ꦽ')
    
    ###
    #hasil = hasil.replace('ꦭꦼ', 'ꦊ')  # tambahkan logika ini jika ingin melakukan sesuatu sebelum mengganti
    #hasil = hasil.replace('ꦫꦼ', 'ꦉ')

    '''
    gunakan seperlunya saja baiknya tidak perlu mengubah settingan berikut
    hasil = hasil.replace('ꦊꦼ', 'ꦊ')  # tambahkan logika ini jika ingin melakukan sesuatu sebelum mengganti
    hasil = hasil.replace('ꦉꦼ', 'ꦉ')
    hasil = hasil.replace('ꦫꦼꦴ', 'ꦉꦴ')
    hasil = hasil.replace('ꦉꦴꦼꦴ', 'ꦉꦴ')
    hasil = hasil.replace('ꦭꦼꦴ', 'ꦋ')
    #tambahkan pengecualian pasangan ḷe dan ṛe untuk la pepet dan nga lelet pakai / zwnj
    hasil = hasil.replace('꧀ꦊ', '꧀ꦭꦼ')
    hasil = hasil.replace('꧀ꦋ', '꧀ꦭꦼꦴ')
    hasil = hasil.replace('ꦿꦼꦴ', 'ꦽꦴ')
    hasil = hasil.replace('ꦿꦼ', 'ꦽ')
    hasil = hasil.replace('ꦽꦴꦼ', 'ꦽꦴ')
    hasil = hasil.replace('ꦽꦼ', 'ꦽ')
    '''

    return hasil