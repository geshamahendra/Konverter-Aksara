import re

def kata_baku(text):
    text = text.replace("/", "\u200C")
    
    #kata tunggal
    text = re.sub(r'\bOṃ\b', 'Ōṃ', text)
    text = re.sub(r'\braja\b', 'rāja', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAwignamastu\b', 'Awighnamāstu', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAwighnamastu\b', 'Awighnamāstu', text, flags=re.IGNORECASE)
    text = re.sub(r'wruh', '\u200cwruh', text, flags=re.IGNORECASE)

    text = re.sub(r'(?<=\b)wong(?=\b)', '‌wwoŋ', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)sabda(?=\b)', 'śabda', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)sarira(?=\b)', 'śarīra', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)mèga(?=\b)', 'mèǥa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)rat(?=\b)', 'rāt', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)bra(?=\b)', 'ƀra', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)bhatara(?=\b)', 'ƀaṭāra', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)sampun(?=\b)', 'sāmpun', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)dewa(?=\b)', 'dèwa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)dewi(?=\b)', 'dèwī', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)sasangka(?=\b)', 'śaśāṅka', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)sri(?=\b)', 'śrī', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)rsi(?=\b)', 'ṛṣi', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)purwa(?=\b)', 'pūrwa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)sirna(?=\b)', 'śīrna', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)puja(?=\b)', 'pūjā', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<=\b)bakti(?=\b)', 'ƀakti', text, flags=re.IGNORECASE)

    #kata yang bisa digabung
    text = re.sub(r'(?i)purna', 'pūrna', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)tirta', 'tīṙŧa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)ningrat', 'niṅrāt', text, flags=re.IGNORECASE)
    #text = re.sub(r'(?i)raja', 'rāja', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)karta', 'kartha', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)resn', 'ṛĕṣṇ', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)mahadewi', 'mahādèwi', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)mahadewa', 'mahādèwa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)puspa', 'puṣpa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)sastra', 'śāstra', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)wisèsa', 'wiśèṣa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)maha', 'mahā', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)wisnu', 'wiṣṇu', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)siwa', 'śīwa', text, flags=re.IGNORECASE)
    #text = re.sub(r'(?i)brahma', 'brāhma', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)ganesha', 'ganèśa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)mataram', 'matāram', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)kresna', 'kṛĕṣṇa', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)budi', 'budđi', text, flags=re.IGNORECASE)

    #Kasus kata diawali vokal harus ditulis upper-lowercase
    text = re.sub(r'\butama\b', 'uttama', text)
    text = re.sub(r'\bUtama\b', 'Uttama', text)
    text = re.sub(r'\bupacara\b', 'uppacara', text)
    text = re.sub(r'\bUpacara\b', 'Uppacara', text)

    return text 

def hukum_aksara(text):
    #kasus sangat spesial dimana 3 huruf sangat sulit dikerjakan di python
    text = re.sub(r'(?<=\w)sṭ(?:h)?(?=\w)', lambda m: 'ṣṫ' if m.group(0).endswith('h') else 'ṣṭ', text)

    # Hukum aksara 
    text = re.sub(r'(?<=^)nḍ(?=\w)', 'ṇḍ', text, flags=re.IGNORECASE)

    text = re.sub(r'\bAi\b', 'Ꜽ', text)
    text = re.sub(r'\bAu\b', 'Ꜷ', text)
    text = re.sub(r'\b^h\b', 'Ꜽ', text)
    
    text = re.sub(r'nḍ', 'ṇḍ', text, flags=re.IGNORECASE)
    text = re.sub(r'nḋ', 'ṇḍ', text, flags=re.IGNORECASE)
    text = re.sub(r'nṭ', 'ṇṭ', text, flags=re.IGNORECASE)
    text = re.sub(r'nṫ', 'ṇṫ', text, flags=re.IGNORECASE)
    text = re.sub(r'nc', 'ñc', text, flags=re.IGNORECASE)
    text = re.sub(r'nj', 'ñj', text, flags=re.IGNORECASE)
    text = re.sub(r'ks', 'kṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'ꝁs', 'ꝁṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'gs', 'gṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'ǥs', 'ǥṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṅs', 'ṅṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'jn', 'jñ', text, flags=re.IGNORECASE)
    text = re.sub(r'rs', 'ṙṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'rĕ', 'ṛĕ', text, flags=re.IGNORECASE)
    text = re.sub(r're', 'ṛĕ', text, flags=re.IGNORECASE)
    text = re.sub(r'rö', 'ṝö', text, flags=re.IGNORECASE)

    return text

def hukum_sigeg(text):
    text = re.sub(r'h(?!\w)', 'ḥ', text, flags=re.IGNORECASE)  
    text = re.sub(r'ng(?=\w)', 'ṅ', text, flags=re.IGNORECASE)  
    text = re.sub(r'ng(?!\w)', 'ŋ', text, flags=re.IGNORECASE)  
    
    return text 

def hukum_ṙ(text):
    daftar_tidak_digandakan = {'n', 'ṅ', 'ṇ', 'h', 'ṣ', 's', 'c', 'ꞓ', 'r', 'ṙ'
                                'ṫ', 'ŧ', 'ꝑ',
                                'ǥ', 'ɉ',  'ƀ', 
                                'ꝁ', 'k', 'ḍ', 'ḋ', 'd', 'đ',}
    
    daftar_vokal = {'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'è', 'o', 'ō', 'ö', 'ŏ', 'ĕ', 'ꜷ', 'ꜽ'} 

    text = re.sub(rf'(?<=\w)r(?=[^{daftar_vokal}])', 'ṙ', text)
    text = re.sub(rf'(?<=ṙ)(?=[{daftar_vokal}])', 'r', text)
    text = re.sub(rf'(?<=ṙ)([a-zḋḍŧṭṣñṇ])', 
                  lambda m: m.group(1) if m.group(1) in daftar_tidak_digandakan else m.group(1) * 2, text)
    text = re.sub(r'(?<=\w)r(?=\s)', 'ṙ', text)

    text = re.sub(r's(?=r[aāiīuūèoöŏĕꜷꜽ])', 'ś', text)

   # Mengganti 'r' + vokal + 's' menjadi 'r' + vokal + 'ṣ', kecuali jika 's' berada di ujung kata
    # Menambahkan pengecekan agar hanya mengganti s jika ada karakter setelah s
    text = re.sub(r'r([' + ''.join(daftar_vokal) + r'])s(?!\s|\b)', r'r\1ṣ', text, flags=re.IGNORECASE)

    #mahaprana
    text = re.sub(r'ṙꝁ', 'ṙkꝁ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙk', 'ṙkk', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙṫ', 'ṙṭṫ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙꝑ', 'ṙpꝑ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙǥ', 'ṙgǥ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙɉ', 'ṙjɉ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙƀ', 'ṙbƀ', text, flags=re.IGNORECASE)

    text = re.sub(r'ṙs', 'ṙṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṛs', 'ṛṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'res', 'ṛĕṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'rĕs', 'ṛĕṣ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙṇ', 'ṙṇṇ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙn', 'ṙṇn', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙd', 'ṙdd', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙđ', 'ṙdđ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙḍ', 'ṙdḍ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙḋ', 'ṙdḋ', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙc', 'ṙcc', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙꞓ', 'ṙcꞓ', text, flags=re.IGNORECASE)

    text = re.sub(r'matuṙṇnuwun', 'matuṙnuwun', text, flags=re.IGNORECASE)
    text = re.sub(r'ṙn', 'ṙṇn', text, flags=re.IGNORECASE)

    #Nanti diganti
    #text = re.sub(r'(\d+)', r':\1:', text)
    
    return text

