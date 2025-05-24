import re
daftar_konsonan = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk"
daftar_vokal = 'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'è', 'é', 'o', 'ō', 'ö', 'ŏ', 'ĕ', 'ꜷ', 'ꜽ', 'â', 'î', 'ê', 'û', 'ô'
vokal_regex = ''.join(daftar_vokal)
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
    r'Ai': 'Ꜽ', r'Au': 'Ꜷ',
    r'ai': 'ꜽ', r'au': 'ꜷ', 
    r'ng': 'ṅ', r'\b^h' : 'ʰ',
    r'\bAwi(g|ǥ)?(h)?namastu\b': 'Awiǥnamāstu', 
    
    r'wi(s|ś)(è|e)sa': 'wiśèṣa',
    r'r(e|è|ĕ)?sn': 'ṛĕṣṇ', r'\bkar(ĕ|e)na': 'karĕṇa', r'\bwau\b': 'wawu',
    r'\bwong\b': 'wwoŋ', r'\bdewa\b': 'dèwa', r'\bdewi\b': 'dèwī',
    r'\bsasangka\b': 'śaśāṅka', r'\b(s|ś)ri\b': 'śrī', r'\brsi\b': 'ṛṣi',
    r'(?i)mahadewi': 'mahādèwi', r'(?i)mahadewa': 'mahādèwa', r'(?i)wisnu': 'wiṣṇu',
    r'(?i)siwa': 'śīwa', r'(?i)ganesha': 'ganèśa', r'(?i)mataram': 'matāram',

    #aturan baku
    r'lĕṅlĕṅ':'lĕŋlĕŋ',
    r'rĕṅrĕṅ':'rĕŋrĕŋ',
    r'sa(ng|ṅ)k(s|ṣ)': 'saŋkṣ',
    r'sa(ng|ṅ)s': 'saŋs',
    r'sa(ng|ṅ)ṣ': 'saŋṣ',
    r'jarkw': 'jar kw', #biasanya ujar ku-
    
    #r'\bnir([' + daftar_konsonan_tanpa_dikecualikan + '])': 'nir\u200c\\1', #nir+zwnj
    #r'\bdur([' + daftar_konsonan_tanpa_dikecualikan + '])': 'dur\u200c\\1', #durr+zwnj

    #sisipkan zwnj setelah imbuhan
    #r'\b(nir|dur|tĕr|bĕr|pĕr)(\w+)': sisipkan_zwnj_setelah_nir_dur,

    #kembalikan setelah imbuhan
    #r'\bp(e|ĕ)rtama\b': 'prĕtama',

    #r'\bnir(w|g|ś)': r'nir\\\1',
    #r'\bpar(w|g|ś)': r'par\\\1',

    #Hukum dwikrama sanskerta
    # Regex substitusi
    r'\b(nir|dur|par|pār)(?![' + vokal_regex + 'bgmjl])' : r'\1\\', #|pur|tir|sir|sar|har|kar|mar|war|yar|gar|bar|ꞓar
    r'\bnir(g)': r'nir\\\1', #nir guna
    r'\bdur\\(y)': r'dur\1', #durya
    r'\bpar\\(w)': r'par\1', #parwa

    #Kasus duhka
    r'(duhk|duhꝁ)([' + vokal_regex + '])' : r'duḥk\2',

    
    #--akhiran
    r'hku\b': 'ḥku', r'hta\b': 'ḥta',
    r'rku\b': 'ṙ\u200cku',


    r'(s|ś)unya': 'śūnya', r'budi': 'budđi', r'purna': 'pūrna', r'hidĕp': 'hiḍĕp', r'rĕsi':'rĕṣi', 
    r'tir(t|ŧ)a': 'tīṙŧa', r'ningrat': 'niṅrāt', r'\bsabda\b': 'śabda',
    r'purwa': 'pūrwa', r'\bsirna\b': 'śīrna', 
    r'\bmurti\b': 'mūrti', r'(ś|s)ighra': 'śīghra', r'prapta': 'prāpta',
    r'\bmus(t|ṭ)i': 'muṣṭi', r'na(th|ŧ)a': 'nāŧa',
    r'prabu': 'praƀu', 
    r'\bmèga\b': 'mèǥa', r'\brat\b': 'rāt',
    r'\bbra\b': 'ƀra', r'\b(bh|ƀ)a(t|ṭ)ar': 'ƀaṭār', r'\bsampun\b': 'sāmpun',
    r'(p|m)uspa': r'\1uṣpa', r'(s|ś)astra': 'śāstra', 
    r'\bwirya': 'wīrya',  
    r'suksma': 'sūkṣma',
    r'\bmaha\b': 'mahā', r'\bmahar(s|ṣ)i\b': 'mahāṙṣi', r'\biswara': 'iśwara',
    r'ramya': 'rāmya', r'(s|ś)iǥra': 'śīǥra', r'saksat': 'sākṣāt',
    r'datĕṅ': 'ḍatĕṅ', r'\bpad(a|ā)': r'paḍ\1',
    r'rana': 'raṇa', r'g(a|u)n(a|ā)': r'g\1ṇ\2', 
    r'm(u|e)sti\b': r'm\1ṣṭi',
    r'hid(ĕ|e)p': 'hiḍĕp', r'yogi(s|ś)wara': 'yogīśwara', r'datĕṅ': 'ḍatĕŋ', r'dusta': 'duṣṭa', 
    r'padaṅ': 'paḍaṅ', r'pandita': 'paṇḍita', r'\bsirna\b': 'śīrna',

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
    r'rana': 'raṇa', r'gana': 'gaṇa', r'guna': 'guṇa', 
    r'musti\b': 'muṣṭi', r'mesti\b': 'meṣṭi', 
    
     r'\braksasa\b': 'rākṣasa',  r'\bsĕdĕṅ\b': 'sĕḍĕŋ',  r'ƀumi': 'ƀūmi', r'rasa': 'raṣa', r'ƀhupati': 'ƀūpati',  r'kala': 'kāla', r'byatita': 'byatīta', #r'tinut\b': 'tinūt', r'\bbyatitan': 'byātītan'
    
'''