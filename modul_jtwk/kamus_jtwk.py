import re
daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
daftar_vokal = "aāiīuūeèéêoōöŏĕꜷꜽâîûô"
# Set vokal untuk pencocokan cepat dalam logika
set_vokal = set(daftar_vokal)
konsonan = '[' + re.escape(daftar_konsonan) + ']'
huruf_dikecualikan = "gblmjy"
daftar_konsonan_tanpa_dikecualikan = daftar_konsonan

for huruf in huruf_dikecualikan:
    daftar_konsonan_tanpa_dikecualikan = daftar_konsonan_tanpa_dikecualikan.replace(huruf, '')
zwnj = "\u200C"


#=======Definisi variabel global============

#Fungsi untuk menyisipkan ZWNJ setelah nir/dur jika sisanya mengandung ≥2 vokal
def sisipkan_zwnj_setelah_nir_dur(match):
    awalan = match.group(1)
    sisanya = match.group(2)
    jumlah_vokal = sum(1 for c in sisanya if c in daftar_vokal)
    if jumlah_vokal >= 2:
        return awalan + '\\' + sisanya  #gunakan \ biar kelihatan, zwnj tidak bisa terlihat
    return awalan + sisanya

substitutions = {
    #Aksara Suci
    r'Ai': 'Ꜽ', r'Au': 'Ꜷ', r'(\*|\#)Om': r'\1Ōṃ',
    r'ai': 'ꜽ', r'au': 'ꜷ', 
    r'ng': 'ṅ', r'\b^h' : 'ʰ',
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
    
    #r'\bnir([' + daftar_konsonan_tanpa_dikecualikan + '])': 'nir\u200c\\1', #nir+zwnj
    #r'\bdur([' + daftar_konsonan_tanpa_dikecualikan + '])': 'dur\u200c\\1', #durr+zwnj

    #sisipkan zwnj setelah imbuhan
    #r'\b(nir|dur|tĕr|bĕr|pĕr)(\w+)': sisipkan_zwnj_setelah_nir_dur,

    #kembalikan setelah imbuhan
    #r'\bp(e|ĕ)rtama\b': 'prĕtama',

    #r'\bnir(w|g|ś)': r'nir\\\1',
    #r'\bpar(w|g|ś)': r'par\\\1',

    #Imbuhan aṅr
    r'\b(m|p)aṅr(\w+)': lambda m: 
        m.group(1) + 'aŋr' + m.group(2) if sum(c in daftar_vokal for c in m.group(2)) >= 2 else m.group(0),
    #Imbuhan aṅ lainnya
    #rf'\b(m|p)aṅ([{daftar_konsonan}])(\w+)': lambda m:    m.group(1) + 'aŋ' + m.group(2) + m.group(3) if sum(c in daftar_vokal for c in m.group(3)) >= 2 else m.group(0),

    #Kasus khusus
    r'(duhk|duhꝁ)([' + daftar_vokal + '])' : r'duḥk\2',  #duhka
    r'rwarw(a|ā|â)' : r'rwa-rw\1', # rwa rwa
    
    #--akhiran
    #khusus ṅ 
    r'(li|sĕḍĕ)ṅk(u|w)':r'\1ŋk\2',
    r'ṅmu\b': r'ŋmu',

    r'h(m|k)(u|w)': r'ḥ\1\2',
    r'r(m|k)(u|w)': r'ṙ\\\1\2',
    r'ht([' + daftar_vokal + r'])\b': r'ḥt\1',
    r'ṅt([' + daftar_vokal + r'])\b': r'ŋt\1',
    
    #spesial kw (ingat ṅ itu ṅku itu gapakai cecak)
    r'([' + daftar_konsonan + '])([' + daftar_vokal + '])r(k|m)w([' + daftar_vokal + '])': r'\1\2ṙ\\\3w\4',
    r'([' + daftar_konsonan + '])([' + daftar_vokal + '])h(k|m)w([' + daftar_vokal + '])': r'\1\2ḥ\3w\4',   

    #Hukum dwikrama sanskerta
    # Regex substitusi
    r'\b(nir|dur|pār)(?![' + daftar_vokal + 'bgmjl])' : r'\1\\', #|pur|tir|sir|sar|har|kar|mar|war|yar|gar|bar|ꞓar
    r'\bnir(g)': r'nir\\\1', #nir guna
    r'\bdur\\(y)': r'dur\1', #durya
    r'\bpar\\(w)': r'par\1', #parwa 
    
    r'(s|ś)unya': 'śūnya', r'budi': 'budđi', 
    r'purna': 'pūrna', r'hidĕp': 'hiḍĕp', r'rĕsi':'rĕṣi', 
    r'tir(t|ŧ)a': 'tīṙŧa', r'\bsabda\b': 'śabda',
    r'purwa': 'pūrwa', r'\bsirna\b': 'śīrna', 
    r'\bmurti\b': 'mūrti', r'(ś|s)ighra': 'śīghra', r'prapta': 'prāpta',
    r'\bmus(t|ṭ)i': 'muṣṭi', r'na(th|ŧ)a': 'nāŧa',
    r'prabu': 'praƀu', 
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
    r'raksasa': 'rākṣasa', r'dat(w|u)': 'ḍat\1',
    r'karana': 'karaṇa', r'\brana\b': 'raṇa',

    

    #bisa merubah wirama
    #r'(ṅ|ng)uni': 'ṅūni',
    #r'nagara': 'nāgara',
    #r'\braja\b': 'rāja',
    #r'\b(s|ś)arira\b': 'śarīra',
    #r'\bpuja\b': 'pūjā', r'rupa\b': 'rūpa', 



    #############################################################
    #backsplash buat pemutus
    r'\\\|': '\u200D',  # input literal \| jadi ZWJ
    r'\\': '\u200C',  # input literal \\ jadi ZWNJ
    #r'`': '\u200C',
    #r'' : ''

    #Pembalik layar-mahaprana
    r'(ṙ|r)kk': r'rk', r'(ṙ|r)kꝁ': r'rꝁ',
    r'(ṙ|r)ṭṫ': r'rṫ', r'(ṙ|r)pꝑ': r'rꝑ',
    r'(ṙ|r)gǥ': r'rǥ', r'(ṙ|r)jɉ': r'rɉ',
    r'(ṙ|r)bƀ': r'rƀ', r'(ṙ|r)ṇṇ': r'rṇ',
    r'(ṙ|r)ṇn': r'rn', r'(ṙ|r)nn': r'rn',
    r'(ṙ|r)dd': r'rd', r'(ṙ|r)dđ': r'rđ', 
    r'(ṙ|r)dḍ': r'rḍ', r'(ṙ|r)dḋ': r'rḋ', 
    r'(ṙ|r)cc': r'rc', r'(ṙ|r)cꞓ': r'rꞓ'
}

'''
#Bahasa Kawi
    r'(s|ś)unya': 'śūnya', r'(?i)budi': 'budđi', r'(?i)purna': 'pūrna',
    r'(?i)tirta': 'tīṙŧa', r'(?i)ningrat': 'niṅrāt', r'\bsabda\b': 'śabda',
    r'purwa': 'pūrwa',  r'\bpuja\b': 'pūjā', r'rupa\b': 'rūpa',
    r'\bmurti\b': 'mūrti', r'(ś|s)ighra': 'śīghra', r'prapta': 'prāpta',
    r'\bmus(t|ṭ)i': 'muṣṭi', r'\bbyatitan': 'byātītan', r'na(th|ŧ)a': 'nāŧa',
    r'prabu': 'praƀu', r'(ṅ|ng)uni': 'ṅūni', r'\bmèga\b': 'mèǥa', r'\brat\b': 'rāt',
    r'\bbra\b': 'ƀra', r'\b(bh|ƀ)a(t|ṭ)ara\b': 'ƀaṭāra', r'\bsampun\b': 'sāmpun',
    r'(?i)puspa': 'puṣpa', r'(?i)sastra': 'śāstra', r'\b(s|ś)arira\b': 'śarīra',
    r'\braja\b': 'rāja', r'\bwirya': 'wīrya', r'nagara': 'nāgara', r'suksma': 'sūkṣma',
    r'\bmaha\b': 'mahā', r'\bmahar(s|ṣ)i\b': 'mahāṙṣi', r'\biswara': 'iśwara',
    r'ramya': 'rāmya', r'(s|ś)iǥra': 'śīǥra', r'saksat': 'sākṣāt',

    #khusus sutasoma
    r'krti\b': 'krĕti', r'\bnrp': 'nrĕp', r'mrti': 'mrĕti', 
    r'rana': 'raṇa',
    
    r'\braksasa\b': 'rākṣasa',  r'\bsĕdĕṅ\b': 'sĕḍĕŋ',  r'ƀumi': 'ƀūmi', r'rasa': 'raṣa', r'ƀhupati': 'ƀūpati',  r'kala': 'kāla', r'byatita': 'byatīta', #r'tinut\b': 'tinūt', r'\bbyatitan': 'byātītan', #r'\bpad(a|ā)': r'paḍ\1',
    #r'rana\b': 'raṇa', #r'g(a|u)n(a|ā)': r'g\1ṇ\2', 
    
'''