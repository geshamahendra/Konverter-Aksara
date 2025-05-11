substitutions = {
    #Aksara Suci
    r'\bOṃ': 'Ōṃ', r'\b(o|O)m\b': '\u200COm\u200C', 
    r'Ai': 'Ꜽ', r'Au': 'Ꜷ',
    r'ai': 'ꜽ', r'au': 'ꜷ', 
    r'ng': 'ṅ',
    r'\bAwi(g|ǥ)?(h)?namastu\b': 'Awiǥnamāstu', 
    
    r'wi(s|ś)(è|e)sa': 'wiśèṣa',
    r'r(e|è|ĕ)?sn': 'ṛĕṣṇ', r'\bkar(ĕ|e)?na': 'karĕṇa', r'\bwau\b': '\u200Dwawu',
    r'\bwong\b': '\u200Dwwoŋ', r'\bdewa\b': 'dèwa', r'\bdewi\b': 'dèwī',
    r'\bsasangka\b': 'śaśāṅka', r'\b(s|ś)ri\b': 'śrī', r'\brsi\b': 'ṛṣi',
    r'(?i)mahadewi': 'mahādèwi', r'(?i)mahadewa': 'mahādèwa', r'(?i)wisnu': 'wiṣṇu',
    r'(?i)siwa': 'śīwa', r'(?i)ganesha': 'ganèśa', r'(?i)mataram': 'matāram',

    #aturan baku
    r'lĕṅlĕṅ':'lĕṅ lĕṅ',
    r'sa(ng|ṅ)s': 'saŋs',
    r'sa(ng|ṅ)ṣ': 'saŋṣ',
    r'sa(ng|ṅ)k': 'saŋk',
    r'\bnir': 'nir',
    #r'\b(a|A)ji\b':'‌Aji',


    r'(s|ś)unya': 'śūnya', r'(?i)budi': 'budđi', r'(?i)purna': 'pūrna',
    r'tir(t|ŧ)a': 'tīṙŧa', r'(?i)ningrat': 'niṅrāt', r'\bsabda\b': 'śabda',
    r'purwa': 'pūrwa', r'\bsirna\b': 'śīrna', r'\bpuja\b': 'pūjā', r'rupa\b': 'rūpa',
    r'\bmurti\b': 'mūrti', r'(ś|s)ighra': 'śīghra', r'prapta': 'prāpta',
    r'\bmus(t|ṭ)i': 'muṣṭi', r'na(th|ŧ)a': 'nāŧa',
    r'prabu': 'praƀu', r'(ṅ|ng)uni': 'ṅūni', r'\bmèga\b': 'mèǥa', r'\brat\b': 'rāt',
    r'\bbra\b': 'ƀra', r'\b(bh|ƀ)a(t|ṭ)ar': 'ƀaṭār', r'\bsampun\b': 'sāmpun',
    r'(?i)puspa': 'puṣpa', r'(s|ś)astra': 'śāstra', r'\b(s|ś)arira\b': 'śarīra',
    r'\braja\b': 'rāja', r'\bwirya': 'wīrya', r'nagara': 'nāgara', r'suksma': 'sūkṣma',
    r'\bmaha\b': 'mahā', r'\bmahar(s|ṣ)i\b': 'mahāṙṣi', r'\biswara': 'iśwara',
    r'ramya': 'rāmya', r'(s|ś)iǥra': 'śīǥra', r'saksat': 'sākṣāt',
    r'datĕṅ': 'ḍatĕṅ', 

    #backsplash buat pemutus
    r'\\\|': '\u200D',  # input literal \| jadi ZWJ
    r'\\': '\u200C',  # input literal \\ jadi ZWNJ
    r'!': '\u200C',
    #r'' : ''
}

'''
#Bahasa Kawi
    r'(s|ś)unya': 'śūnya', r'(?i)budi': 'budđi', r'(?i)purna': 'pūrna',
    r'(?i)tirta': 'tīṙŧa', r'(?i)ningrat': 'niṅrāt', r'\bsabda\b': 'śabda',
    r'purwa': 'pūrwa', r'\bsirna\b': 'śīrna', r'\bpuja\b': 'pūjā', r'rupa\b': 'rūpa',
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
    r'hid(ĕ|e)p': 'hiḍĕp', 
    r'\bpada\b': 'paḍa', r'\braksasa\b': 'rākṣasa',  r'\bsĕdĕṅ\b': 'sĕḍĕŋ', r'pandita': 'paṇḍita', r'ƀumi': 'ƀūmi', r'rasa': 'raṣa', r'ƀhupati': 'ƀūpati', r'yogi(s|ś)wara': 'yogīśwara', r'datĕṅ': 'ḍatĕŋ', r'dusta': 'duṣṭa', 
    r'padaṅ': 'paḍaṅ', r'kala': 'kāla', r'byatita': 'byatīta', #r'tinut\b': 'tinūt', r'\bbyatitan': 'byātītan'
    
'''