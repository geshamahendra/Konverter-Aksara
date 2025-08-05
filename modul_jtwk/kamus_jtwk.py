import re
daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
daftar_vokal = "aāiīuūeèéêoōöŏĕꜷꜽâîûô"
# Set vokal untuk pencocokan cepat dalam logika
set_vokal = set(daftar_vokal)
konsonan = '[' + re.escape(daftar_konsonan) + ']'
huruf_dikecualikan = "gblmjy"
daftar_konsonan_tanpa_dikecualikan = daftar_konsonan
SH = '\u00AD' #soft hypen

for huruf in huruf_dikecualikan:
    daftar_konsonan_tanpa_dikecualikan = daftar_konsonan_tanpa_dikecualikan.replace(huruf, '')
zwnj = "\u200C"

substitutions = {
    #Aksara Suci
    'Ai': 'Ꜽ', 'Au': 'Ꜷ', r'(\*|\#)Om': r'\1Ōṃ',
    'ai': 'ꜽ', 'au': 'ꜷ', 
    'ng': 'ṅ', r'\b^h' : 'ʰ',
    r'\b(A|a)wi(g|ǥ)?(h)?namastu\b': r'`Awiǥnamāstu', 
    
    r'wi(s|ś)(è|e)sa': 'wiśèṣa',
    r'r(e|è|ĕ)?sn((?![' + daftar_konsonan + ']))': r'ṛĕṣṇ\2', 
    r'\bkar(ĕ|e)na': 'karĕṇa', r'\bwau\b': 'wawu',
    r'\bwong\b': 'wwoŋ', r'\bdewa\b': 'dèwa', r'\bdewi\b': 'dèwī',
    r'\bsasangka\b': 'śaśāṅka', r'\b(s|ś)r(i|ī)\b': 'śrī', r'\brsi\b': 'ṛṣi',
    r'(?i)mahadewi': 'mahādèwi', r'(?i)mahadewa': 'mahādèwa', r'(?i)wisnu': 'wiṣṇu',
    r'(?i)siwa': 'śīwa', r'(?i)ganesha': 'ganèśa', r'(?i)mataram': 'matāram',

    #aturan baku
    r'lĕṅlĕṅ':'lĕŋlĕŋ',
    r'rĕṅrĕṅ':'rĕŋrĕŋ',
    r'\bsa(ng|ṅ)k(s|ṣ)(e|è|é)pa': 'saŋkṣepa',
    r'\bsa(ng|ṅ)sipta': 'saŋsipta',
    r'\bsa(ng|ṅ)ṣipta': 'saŋṣ',
    r'ṅkt': 'ŋkt',

    # Hukum Imbuhan sanskrit
    # Regex substitusi
    r'\b(nir|dur|pār|dūr)(?![' + daftar_vokal + 'bgmjl])' : r'\1\\', #|pur|tir|sir|sar|har|kar|mar|war|yar|gar|bar|ꞓar
    r'\bnir(g)': r'nir\\\1', #nir guna
    r'\bdur\\(y|n)': r'dur\1', #durya
    r'\bpar\\(w)': r'par\1', #parwa 

    rf'(pĕr|bĕr|tĕr|mĕṅ)([{daftar_konsonan}])(\w*)':
        lambda m: f'{m.group(1)}{SH}{m.group(2)}{m.group(3)}'
        if sum(c in daftar_vokal for c in m.group(3).lower()) > 1 else m.group(0),

    #Imbuhan aṅr
    r'\b(m|p)aṅr(\w+)': lambda m: 
        m.group(1) + f'aŋ{SH}r' + m.group(2) if sum(c in daftar_vokal for c in m.group(2)) >= 2 else m.group(0),
    #Imbuhan aṅ lainnya
    rf'\b(m|p)aṅ((?![gk])[{daftar_konsonan}])(\w+)': lambda m:    m.group(1) + 'aŋ' + m.group(2) + m.group(3) if sum(c in daftar_vokal for c in m.group(3)) >= 2 else m.group(0),

    #Kasus khusus
    r'(duhk|duhꝁ)([' + daftar_vokal + '])' : r'duḥk\2',  #duhka
    r'rwarw(a|ā|â)' : r'rwa-rw\1', # rwa rwa
    
    #--akhiran
    #khusus ṅ 
    r'(li|sĕḍĕ)ṅk(u|w)':r'\1ŋk\2',
    r'ṅmu\b': r'ŋmu',
    r'ṅt([' + daftar_vokal + r'])\b': r'ŋt\1',
    r'ṅ\\': r'ŋ',

    #khusus r dan h
    r'h(m|k)(u|w)': r'ḥ\1\2',
    r'r(m|k)(u|w)': r'ṙ\\\1\2',
    r'rt([' + daftar_vokal + r'])\b': r'r\\t\1',
    r'ht([' + daftar_vokal + r'])\b': r'ḥt\1',
    r'([' + daftar_vokal + r'])r(w|b)ud(a|ā)' : r'\1r\\\2ud\3',
    

    #spesial kw (ingat ṅ itu ṅku itu gapakai cecak)
    r'([' + daftar_konsonan + '])([' + daftar_vokal + '])r(k|m)w([' + daftar_vokal + '])': r'\1\2ṙ\\\3w\4',
    r'([' + daftar_konsonan + '])([' + daftar_vokal + '])h(k|m)w([' + daftar_vokal + '])': r'\1\2ḥ\3w\4', 

    #Bahasa Indonesia
    rf'([{daftar_vokal}])([{daftar_konsonan}])lah\b': r'\1\2 laḥ',  
    
    r'\b(s|ś)unya': 'śūnya', r'budi': 'budđi', 
    r'purna': 'pūrna', r'hidĕp': 'hiḍĕp', r'rĕsi':'rĕṣi', 
    r'tir(t|ŧ)a': 'tīṙŧa', r'\bsabda\b': 'śabda',
    r'purwa': 'pūrwa', r'\bsirna\b': 'śīrna', 
    r'\bmurti\b': 'mūrti', r'(ś|s)ighra': 'śīghra', r'prapta': 'prāpta',
    r'\bmus(t|ṭ)i': 'muṣṭi', r'na(th|ŧ)a': 'nāŧa',
    r'prabu': 'praƀu', r'\bguna\b': 'guṇa', 
    r'\bmèga\b': 'mèǥa', r'\brat\b': 'rāt',
    r'\bbra\b': 'ƀra', r'\b(bh|ƀ)a(t|ṭ)ar': 'ƀaṭār', r'\bsampun\b': 'sāmpun',
    r'(p|m)uspa': r'\1uṣpa', r'(s|ś)astra': 'śāstra', 
    r'\bwirya': 'wīrya',  
    r'suksma': 'sūkṣma',
    r'\bmaha': 'mahā', r'\bmahar(s|ṣ)i': 'mahāṙṣi', r'\biswara': 'iśwara',
    r'ramya': 'rāmya', r'(s|ś)iǥra': 'śīǥra', r's(a|ā)k(s|ṣ)(a|ā)t': 'sākṣāt',
    r'datĕṅ': 'ḍatĕṅ', 
    r'm(u|e)sti\b': r'm\1ṣṭi',
    r'hid(ĕ|e)p': 'hiḍĕp', r'yogi(s|ś)wara': 'yogīśwara', r'datĕṅ': 'ḍatĕŋ', r'dusta': 'duṣṭa', 
    r'padaṅ': 'paḍaṅ', r'pandita': 'paṇḍita', r'\bsirna\b': 'śīrna', r'\bsarira': 'śarīra', r'atmaj': 'ātmaj',
    r'raksasa': 'rākṣasa', r'dat(w|u)': r'ḍat\1',
    r'karana': 'karaṇa', r'\brana\b': 'raṇa',

    #bisa merubah wirama
    r'(ṅ|ng)uni': 'ṅūni',
    r'nagara': 'nāgara',
    r'\braja\b': 'rāja',
    r'\b(s|ś)arira\b': 'śarīra',
    r'\bpuja\b': 'pūjā', r'rupa\b': 'rūpa',
    r'\blila\b': 'lilā',  r'\brat\b': 'rāt',

    #############################################################
    #backsplash buat pemutus
    r'\\\|': '\u200D',  # input literal \| jadi ZWJ
    r'\\': '\u200C',  # input literal \\ jadi ZWNJ

    #Pembalik layar-mahaprana
    r'(ṙ|r)kk': r'rk', r'(ṙ|r)kꝁ': r'rꝁ',
    r'(ṙ|r)ṭṫ': r'rṫ', r'(ṙ|r)pꝑ': r'rꝑ',
    r'(ṙ|r)gǥ': r'rǥ', r'(ṙ|r)jɉ': r'rɉ',
    r'(ṙ|r)bƀ': r'rƀ', r'(ṙ|r)ṇṇ': r'rṇ',
    r'(ṙ|r)ṇn': r'rn', r'(ṙ|r)nn': r'rn',
    r'(ṙ|r)dd': r'rd', r'(ṙ|r)dđ': r'rđ', 
    r'(ṙ|r)dḍ': r'rḍ', r'(ṙ|r)dḋ': r'rḋ', 
    r'(ṙ|r)cc': r'rc', r'(ṙ|r)cꞓ': r'rꞓ',
    r'(ṙ|r)tŧ': r'rŧ',

    #khusus ṙṇṇ tidak ada di jawa kuno
    r'(ṙ|r)ṇ': r'rn',

}