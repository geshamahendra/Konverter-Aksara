from modul_jtwk.konstanta import DAFTAR_VOKAL, DAFTAR_KONSONAN, SH

substitutions = {
    #Aksara Suci
    'Ai': 'Ꜽ', 'Au': 'Ꜷ', r'(\*|\#)[Oo]m': r'\1Ōṃ',
    'ai': 'ꜽ', 'au': 'ꜷ', 
    'ng': 'ṅ', r'\b^h' : 'ʰ',

    #Pembalik layar-mahaprana
    rf'[rṙᶉ]([{DAFTAR_KONSONAN.replace("t","").replace("w","")}])\1': r'r\1', 
    r'[rṙ]kk': r'rk', r'[rṙ]ṭṫ': r'rṫ', 
    r'[rṙ]gǥ': r'rǥ', r'[rṙ]bƀ': r'rƀ', 
    r'[rṙ]ṇn': r'rn', r'[rṙ]dd': r'rd', 
    r'[rṙ]dḍ': r'rḍ', r'[rṙ]cc': r'rc', 
    r'[rṙ]tŧ': r'rŧ', r'[rṙ]kꝁ': r'rꝁ',
    r'[rṙ]pꝑ': r'rꝑ', r'[rṙ]jɉ': r'rɉ',
    r'[rṙ]ṇṇ': r'rṇ', r'[rṙ]nn': r'rn',
    r'[rṙ]dđ': r'rđ', r'[rṙ]dḋ': r'rḋ',
    r'[rṙ]cꞓ': r'rꞓ',  

    #khusus ṙṇṇ tidak ada di jawa kuno
    r'[rṙ]ṇ': r'rn',

    #===================#

    r'\b[Aa]wi[gǥ]?(h)?namastu\b': r'`Awiǥnamāstu',
    r'[sś][aā]nti': r'śānti', 
    r'r[eèĕ]?sn((?![' + DAFTAR_KONSONAN + ']))': r'rĕṣṇ', 
    
    #aturan baku
    r'lĕṅlĕṅ':'lĕŋlĕŋ', r'nuṅ(s|t)uṅ':r'nuŋ\1uṅ',
    r'rĕṅrĕṅ':'rĕŋrĕṅ',

    #en dash khusus
    r'(rĕs)(?: |-)(?=rĕs)': r'\1–',

    r'\bsa[ṅn]k[sṣ][eèé]pa': 'saŋkṣepa',
    rf'\bsa[nṅ](s|ṣ)ipt([{DAFTAR_VOKAL}])': r'saŋ\1ipt\2',
    r'\bsa[n|ṅ]ṣipta': 'saŋṣ',
    r'ṅkt': 'ŋkt', r'ṅ[ṣs][ṭt]r': 'ŋṣṭr', rf'ṅsk': r'ŋsk',
    
    #suku kata khusus
    #rf'\b([{DAFTAR_KONSONAN}]+)a([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ā\2',
    #rf'\b([{DAFTAR_KONSONAN}]+)i([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ī\2',
    #rf'\b([{DAFTAR_KONSONAN}]+)u([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ū\2',
    #rf'\b([{DAFTAR_KONSONAN}]+)ĕ([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ö\2',
    
    # Hukum Imbuhan sanskrit
    # Regex substitusi
    r'\b(nir|dur|pār|dūr)(?![' + DAFTAR_VOKAL + 'bngmjl])' : r'\1\\', #|pur|tir|sir|sar|har|kar|mar|war|yar|gar|bar|ꞓar
    r'\bnir(g)': r'nir\\\1', #nir guna
    r'\bnir(l)': r'nir\\\1', #nir labha
    r'\bdur\\(y|n)': r'dur\1', #durya
    r'\bpar\\(w)': r'par\1', #parwa 

    rf'\b(pĕr|bĕr|tĕr|mĕṅ)([{DAFTAR_KONSONAN}])(\w*)':
        lambda m: f'{m.group(1)}{SH}{m.group(2)}{m.group(3)}'
        if sum(c in DAFTAR_VOKAL for c in m.group(3).lower()) > 1 else m.group(0),

    # Imbuhan aṅr / āṅr
    r'(?:\b(m|p)aṅr|(\w+)āṅr|([{DAFTAR_KONSONAN}]) aṅr)(\w+)': lambda m: (
        (m.group(1) or m.group(2) or m.group(3)) +
        ('aŋ' if m.group(1) or m.group(3) else 'āŋ') +
        r'r' + m.group(4)
        if sum(c in DAFTAR_VOKAL for c in m.group(4)) >= 2 else m.group(0)
    ),

    # Imbuhan aṅrw / āṅrw[aā]
    r'(?:\b(m|p)aṅrw|(\w+)āṅrw|([{DAFTAR_KONSONAN}]) aṅrw)(a|ā)': lambda m: (
        (m.group(1) or m.group(2) or m.group(3)) +
        ('aŋ' if m.group(1) or m.group(3) else 'āŋ') +
        r'\rw' + m.group(4)
    ),
    
    # Imbuhan aṅrĕ
    r'(?:\b(m|p)aṅrĕ|(\w+)āṅrĕ|([{DAFTAR_KONSONAN}]) aṅrĕ)(e|ĕ)': lambda m: (
        (m.group(1) or m.group(2) or m.group(3)) +
        ('aŋ' if m.group(1) or m.group(3) else 'āŋ') +
        rf'{SH}rĕ' + m.group(4)
    ),

    # Imbuhan aṅ lainnya (selain g/k), dipecah jadi dua
    # Imbuhan aṅ intra-kata (tidak melibatkan konsonan + spasi)
    rf'(?:\b(m|p)aṅ|(\w+)āṅ)((?![gk])[{DAFTAR_KONSONAN}])(\w+)': (
        lambda m: (
            (m.group(1) or m.group(2))
            + ('aŋ' if m.group(1) else 'āŋ')
            + m.group(3) + m.group(4)
            if sum(c in DAFTAR_VOKAL for c in m.group(4)) >= 2
            else m.group(0)
        )
    ),
    # Imbuhan aṅ antar-kata (konsonan + spasi + aṅ)
    rf'([{DAFTAR_KONSONAN}])[^\S\n]+aṅ((?![gk])[{DAFTAR_KONSONAN}])(\w+)': (
        lambda m: (
            m.group(1)+ ' '+ 'aŋ'+ m.group(2)+ m.group(3)
            if sum(c in DAFTAR_VOKAL for c in m.group(3)) >= 2
            else m.group(0)
        )
    ),

    #aṅ sastra lampah diawali konsonan rangkap
    rf'(r[wy])aṅ((?![gk])[{DAFTAR_KONSONAN}])(\w+)': (
        lambda m: (
            m.group(1)
            + 'aŋ'
            + m.group(2)
            + m.group(3)
            if sum(c in DAFTAR_VOKAL for c in m.group(3)) >= 2
            else m.group(0)
        )
    ),

    #pendekkan akhiran ān
    rf'\b(\w+)(ān)([^\S\n]+[{DAFTAR_KONSONAN}])': (
        lambda m: (
            m.group(1) + 'an' + m.group(3)
            if sum(c in DAFTAR_VOKAL for c in m.group(1)) > 0
            else m.group(0)
        )
    ),

    #tambahan aṅ khusus
    r'aṅ(jrah)\b': r'aŋ\1',
    r'(\w)āṅ(jrah)\b': r'\1āŋ\2',

    #rf'\bm([āa])r([{DAFTAR_KONSONAN}])': r'mar\\\2',

    #Kasus khusus
    r'duh(k|ꝁ)(ita|[' + DAFTAR_VOKAL + '])' : r'duḥꝁ\2', #duhka duhkita
    r'rwarw(a|ā|â)' : r'rwa-rw\1', # rwa rwa
    r'\b(p|m)?aṅlĕ' : r'\1a lĕ',
    r'(ā|a)ḥniṅ\b' : r'\1hniṅ',
    r'\bmasku\b' : r'māsku',

    #=================#

    #pemanjang vokal suku kata tunggal diapit konsonan
    #rf'\b([{DAFTAR_KONSONAN}])a([{DAFTAR_KONSONAN}]\s*[{DAFTAR_KONSONAN}])': r'\1ā\2',
    #rf'\b([{DAFTAR_KONSONAN}])i([{DAFTAR_KONSONAN}]\s*[{DAFTAR_KONSONAN}])': r'\1ī\2',
    #rf'\b([{DAFTAR_KONSONAN}])u([{DAFTAR_KONSONAN}]\s*[{DAFTAR_KONSONAN}])': r'\1ū\2',

    #=============================

    #akhiran khusus
    r'ṅ(ni|nira|nire|nik|)(ṅ?)\b': r'ŋ\1\2',
    r'h(ni|nira|nire|nik)(ṅ?)\b': r'ḥ\1\2',
    r'r(ni|nira|nire|nik)(ṅ?)\b': r'r\\\1\2',
    #rf'ṅny([{DAFTAR_VOKAL}])': r'ŋ\\ny\1',
    #rf'hny([{DAFTAR_VOKAL}])': r'ḥ\\ny\1',
    #rf'ṙny([{DAFTAR_VOKAL}])': r'ṙ\\ny\1',

    #rf'h(nik[{DAFTAR_VOKAL}]|nir[{DAFTAR_VOKAL}]|niṅ)': r'ḥ\1',
    #rf'ṅ(nik[{DAFTAR_VOKAL}]|nir[{DAFTAR_VOKAL}]|niṅ)': r'ŋ\1',
    #rf'r(nik[{DAFTAR_VOKAL}]|nir[{DAFTAR_VOKAL}]|niṅ)': r'ṙ\1',
    
    #spesial kw (ingat ṅ itu ṅku itu gapakai cecak)
    r'([' + DAFTAR_KONSONAN + '])([' + DAFTAR_VOKAL + '])r(k|m)w([' + DAFTAR_VOKAL + '])': r'\1\2ṙ\\\3w\4',
    r'([' + DAFTAR_KONSONAN + '])([' + DAFTAR_VOKAL + '])h(k|m)w([' + DAFTAR_VOKAL + '])': r'\1\2ḥ\3w\4', 
    
    #khusus ry
    r'\bduryan\b': 'dūryan', r'\daryas\b': 'dāryas',

    r'\b[aā]d[bƀ]u[tŧ]': 'adƀut', 
    rf'([{DAFTAR_KONSONAN}])[aā]d[bƀ][uū][tŧ]': r'\1ādƀut', #adbhutha
    r'\bky[aā]t[iī]\b': 'ꝁyāti', r'\bky[aā]t(iī)(\w)': r'ꝁyāt\1\2', 
    r'muka': 'muꝁa', rf'muk([{DAFTAR_VOKAL}])(\w)': r'muꝁ\1\2',

    r'\bkar[ĕe]na': 'karĕṇa', r'\bwau\b': 'wawu',
    r'\bwong\b': 'wwoŋ', r'\bṅka': 'ṅkā', r'ndĕ([ms])': r'nḍĕ\1',
    r'nadah': r'naḍah',
    r'\bsasa[nṅ]ka\b': 'śaśāṅka', r'\b[ṣsś]r[iī]\b': 'śrī', r'\brsi\b': 'ṛṣi',
    r'siwa': 'śīwa', r'ganesha': 'ganèśa', r'mataram': 'matāram',
    r'wi[sś][èe]sa': 'wiśèṣa', r'\bmas\b': 'mās', r'dosa': 'doṣa', r'\blati': 'laṭi',
    r'[tṭŧ]a[tṭŧ]it': 'taṭit',
    

    r'nirb[āa][nṇ](a|ā)': r'nirbāṇ\1',

    r'[iī][sś]wara': 'īśwara',
    r'e[sś]wara': 'eśwara',
    
    rf'\bđanur([{DAFTAR_KONSONAN}])': r'đanur\\\1',
    r'punarƀawa': r'punar\\ƀawa',
    rf'catur([{DAFTAR_KONSONAN}])': r'catur\\\1',

    r'\bs[uū]n(u|w)': r'sūn\1', #sunu=putra
    r'dat(w|u)': r'ḍat\1',
    r'(p|m)[uū]sp': r'\1uṣp',
    r'(\w)aṅde\b': r'\1āṅde',
    
    r'[sś]unya': 'śūnya', r'budi': 'budđi', r'ƀasm': 'ƀaṣm', 
    r'purna': 'pūrna', r'hidĕp': 'hiḍĕp', r'rĕsi':'rĕṣi', 
    r'purwa': 'pūrwa', r'[sś][iī]rna': 'śīrna', 
    r'murt(t)?([iy])': r'mūrtt\2',
    r'kirt(t)?([iy])': r'kīrtt\2', 
    r'prapta': 'prāpta',
    r't[iī]k[sṣ][nṇ]': 'tīkṣṇ',
    r'\b(mu|minu)[sṣ][tṭ]i': r'\1ṣṭi', 
    r'naŧa': 'nāŧa',
    r'prabu': 'praƀu', r'gun(a|ā)': r'guṇ\1', 
    r'\bmèga\b': 'mèǥa', r'\brat\b': 'rāt',
    r'\bbra\b': 'ƀra', r'\b[bƀ]a[tŧṭ]ar': 'ƀaṭār', r'\bs[aā]mpun\b': 'sampun', r'wakpatu': 'wākpaṭu', 
    r'\bwirya': 'wīrya', r'wisa': 'wiṣa', #r'\brasa\b': 'raṣa', 
    r'uksma': 'ūkṣma', r'\bs[eĕ][dḍ][eĕ]ṅ\b': 'sĕḍĕṅ',
    r'\bmaha(?!ntĕn)': 'mahā', 
    r'\bmahar[sṣ]i': 'mahāṙṣi',

    r'\b[ƀb][aā][sṣ]a': 'ƀaṣa',
    
    r'\bi[sś]wara': 'iśwara', 
    r'r[aā][sṣś]mi': 'raśmi',
    r'r[aā]mya': 'ramya', r'[sś]iǥra': 'śīǥra', r's[aā]k[sṣ][aā]t': 'sākṣāt', r'maṅsa': 'māṅsa',
    r'[dḍ]at[ĕe]ṅ': 'ḍatĕṅ', r'ratri': 'rātri', 
    r'm(u|e)sti\b': r'm\1ṣṭi',
    r'hid(ĕ|e)p': 'hiḍĕp', r'yogi[sś]wara': 'yogīśwara', r'dusta': 'duṣṭa', r'makuta': 'makuṭa', r'man(i|ī)': r'maṇ\1',  r'\bsirna\b': 'śīrna', r'\b[sś]ar[iī]ra': 'śarīra', r'atma': 'ātma', r'pranata': 'praṇata',  r'sꝑatik': 'sꝑaṭik', 
    r'k(a|ā)r(a|ā)na': r'k\1r\2ṇa',  r'patni': 'patnī', r'drĕ[ḍđ]a': 'drĕḋa', r'saṅkya': 'saṅꝁya', r'bakti': 'ƀakti', r'nipuna': 'nipuṇa', r'ƀarana': 'ƀaraṇa', r'ka[tṭ][uū][nṅ]ka': 'kaṭuṅka',
    r'(?<!~)\brana\b': 'raṇa', 
    
    r'(?<!ga)gana\b': r'gaṇa', r'\bgana\b': r'gaṇa',
    r'raksasa': 'rākṣasa', r'samānta': r'samanta',
    r'r[aā]ksa(\w?)\b': r'rakṣa\1', r'kĕdap': 'kĕḍap',
    r'k([ou])t([iy])': r'k\1ṭ\2', r'paramarŧa': 'paramārŧa',
    
    r'ksana': 'kṣaṇa', r'\bb([aā])na': r'b\1ṇa',
    r'osad': 'oṣad', r'bhagya': 'bhāgya', r'k[sṣ]a[ṇn]': 'kṣaṇ',
    r'ƀaskar': 'ƀaṣkar', r'dĕp': 'ḍĕp', r'k[aā]n[tṭ]a': 'kaṇṭa', r'br[aā]hm': 'brahm', r'\byasa\b': 'yaśa', r'esti\b': 'eṣṭi', 
    
    r'pudak': 'puḍak', r'aṅin(\s?)dar[aā]t': 'aṅiṇḍarat', r'darat': 'ḍarat', r'([tn])unda': r'\1unḍa', r'kinanta': 'kinanṭa',
    r'g[eĕ][nṇ][dḍ]iṅ': 'gĕṇḍiṅ', r'duduk': 'ḍuḍuk', r'li[nṇ][dḍ](u|ū|w)': r'linḍ\1', r't[eĕ][dḍ][uū]([n])': r'tĕḍu\1',  
    r'tum[eĕ][dḍ][uū]([n])': r'tumĕḍu\1',
    r'padaṅ': 'paḍaṅ', r'tindih': 'tinḍih', r'dukuh': 'ḍukuh', r'undu([tk])': r'unḍu\1', r'ĕdap\b': r'ĕḍap', 
    r'danda': 'ḍanḍa', r'garuda': 'garuḍa', r'tadah': 'taḍah', r'p[āa]n[dḍ]aw': 'pānḍaw', 
    r'tĕndas': 'tĕnḍas', r'mandala': 'manḍala', r'gandewa': 'ganḍewa', r'manda\b': 'manḍa', r'tanda': 'tanḍa',
    
    r'\brasmi': 'raṣmi', 
    r'r[aā]tn[aā]' : 'ratna', r'ratnakanda': r'ratnakanḍa',
    r'\bsaj(ñ|n)[aā]': 'sajñā', r'pra[bƀ][aā]wa': 'praƀāwa', r'\bk[aā][sś]mala': 'kaśmala', 
    
    r'g(ĕ|a)d(a|u|i)ṅ': r'g\1ḍ\2ṅ', 
    r'p(i|u)nd(a|u)': r'p\1nḍ\2',
    r'pininda': r'pininḍa', r'(ta|sa)[nṇ]diṅ': r'\1ṇḍiṅ', r'pandan': r'panḍan', r'gundik': r'gunḍik', r'k[eĕ]ndaṅ': r'kĕnḍaṅ', 

    #pendekkan
    r'\bs[aā]smrĕti': 'sasmrĕti',  r'c[iī]tta': 'citta',
    r'pāksa': 'paksa', r'wākt(r?)a': r'wakt\1a', r'\b[sś][uū]kl': 'śukl',  
    r'\bārja': 'arja', r'(\w{2,})[āa]rja': r'\1ārja', 
    r'mātya': 'matya', r'māntuk': 'mantuk', 
    r'd[iī](b|w)ya': r'di\1ya', r'[ƀb][uū]kt(i|y)': r'ƀukt\1',
    r's[aā]nma[tŧ]a': 'sanmata',  r'ma[nṇ][iī]ndr': 'maṇīndr', 
    r'k[aā]sturi': 'kasturi', r'wiwāk[sṣ]an': 'wiwaksan', r'wārga': 'warga', 

    #konsonan ganda
    r'm[aā]rtyaloka': 'marttyaloka', r't[aā]twa': 'tattwa', r'jag[aā]ttraya': 'jagattraya', 
    rf'b[aā][hḥ]n([{DAFTAR_VOKAL}]|y)': r'bahn\1', 
    rf'[sś][aā]str([{DAFTAR_VOKAL}])': r'śāstr\1', 
    rf's[aā]ṅsay([{DAFTAR_VOKAL}])': r'saṅśay\1',
    rf'p[aā]n[ḍd]it([{DAFTAR_VOKAL}])': r'paṇḍit\1',
    rf'[śs][iī][gǥ]r([{DAFTAR_VOKAL}])': r'śīǥr\1',
    rf'by[aā]kt([{DAFTAR_VOKAL}])': r'byakt\1',
    rf'r[aā]jy([{DAFTAR_VOKAL}])': r'rājy\1',
    rf'pra[nṇ][aā]my([{DAFTAR_VOKAL}])': r'praṇamy\1',
    rf'c[iī]tt([{DAFTAR_VOKAL}])': r'citt\1',
    rf'tap[aā]sw([{DAFTAR_VOKAL}])': r'tapasw\1',
    rf's[aā]ks([{DAFTAR_VOKAL}])': r'sākṣ\1',
    rf'm[uū]r[kꝁ]([{DAFTAR_VOKAL}])': r'mūrꝁ\1',
    rf'sw[aā]pn([{DAFTAR_VOKAL}])': r'swapn\1',
    rf'ǥurnit([{DAFTAR_VOKAL}])': r'ǥūrnit\1',
    rf'mūḍ([{DAFTAR_VOKAL}])': r'mūḋ\1',
    rf't[iī]r[tŧ]([{DAFTAR_VOKAL}])': r'tīṙŧ\1', 
    rf's[aā]bd([{DAFTAR_VOKAL}])': r'śabd\1',
    rf'māstw([{DAFTAR_VOKAL}])': r'mastw\1',
    rf'[sś]ara[nṇ]([{DAFTAR_VOKAL}])': r'śaraṇ\1',
    rf'\b[aā]sy([{DAFTAR_VOKAL}])': r'āsy\1',  
    rf'karun([{DAFTAR_VOKAL}])': r'karuṇ\1',  
    rf'lak[sṣ]a[nṇ]([{DAFTAR_VOKAL}])': r'lakṣaṇ\1',  
    rf'd[aā]k[sṣ]i[nṇ]([{DAFTAR_VOKAL}])': r'dakṣiṇ\1',
    rf'm[aā]nu[sṣ]([{DAFTAR_VOKAL}])': r'mānuṣ\1',
    rf'n[iī]st([{DAFTAR_VOKAL}])': r'niṣṭ\1',
    rf'(go|ƀra|tu)st([{DAFTAR_VOKAL}])': r'\1ṣṭ\2',
    rf'makut([{DAFTAR_VOKAL}])': r'makuṭ\1',
    rf'wisn([{DAFTAR_VOKAL}]|w)': r'wiṣṇ\1',
    rf'p([ou])rus([{DAFTAR_VOKAL}])': r'p\1ruṣ\2',
    rf'k(a|ā)ra[nṇ]([{DAFTAR_VOKAL}])': r'k\1raṇ\2',
    rf'muky([{DAFTAR_VOKAL}])': r'muꝁy\1',
    rf'(?<!u)r([{DAFTAR_VOKAL}])n([{DAFTAR_VOKAL.replace("ĕ","")}])': r'r\1ṇ\2',
    rf'pa[dḍ]([{DAFTAR_VOKAL}])': r'paḍ\1',
    
      
    #bisa merubah wirama
    r'ṅuni': 'ṅūni', r'\brah\b' : 'rāh',
    r'nagara': 'nāgara', r'pat\b': 'pāt',
    r'\bsad\b': 'ṣaḍ',
    r'\brum': 'rūm', r'tut': 'tūt', r'tinut': 'tinūt',
    r'\bsyuh\b': 'syūh',
    r'\braja\b': 'rāja',
    r'\b[sś]arira': 'śarīra',
    r'puja': 'pūjā', r'rupa': 'rūpa',
    r'\blila\b': 'lilā',  r'\brat\b': 'rāt',
    r'[bƀ][uū][sṣ][aā][nṇ]': 'ƀūṣaṇ',
    r'[bƀ][iī][sṣ][aā][nṇ]': 'ƀīṣaṇ',

    #===============#
    #akhiran
    #khusus ṅ 
    r'(sĕḍĕ)ṅk(u|w)':r'\1ŋk\2',
    r'ṅmu\b': r'ŋmu',
    r'ṅt([' + DAFTAR_VOKAL + r'](n|ŋ)?)\b': r'ŋt\1',
    r'ṅ\\': r'ŋ',
    r'ṅ(ni|nira|nire|nik)(ṅ?)': r'ŋ\1\2',

    #khusus r dan h
    r'h(m|k)(u|w)': r'ḥ\1\2',
    r'r(m|k)(u|w)': r'ṙ\\\1\2',
    r'rta\b': r'ṙ ta',
    r'ht([' + DAFTAR_VOKAL + r'](n|ŋ|ṅ)?)\b': r'ḥt\1',
    r'([' + DAFTAR_VOKAL + r'])r(w|b)ud(a|ā)' : r'\1r\\\2ud\3',

    #vokal awal atau suku kata terbuka
    r'\b[aā](kral|kweh|rđ|ṅlih|gya|mbĕk|[sś]ray|psara|mrĕta|mrih|ntara|stra|gra|hyun|ntaka|glis|krak|sraṅ|sya|ksi)': r'a\1', 
    r'(?<!nir)[aā](kral|kweh|rđ|ṅlih|gya|mbĕk|psara|mrĕta|mrih|ntara|stra|gra|hyun|ntaka|glis|krak|sraṅ|sya|ksi)': r'ā\1',
    r'\b[iī](ndra)': r'i\1', 
    r'(?<!nir)[iī](ndra)': r'ī\1',

    

    #############################################################

    #pemisah kata ulang
    r'\b([A-Za-z]{2,}?)(?=(?!–)\1\b)' : r'\1-',# kecualikan en dash
    #kembalikan kata ulang
    r'\b(sum)-\1': r'\1\1',

    #backsplash buat pemutus
    r'\\\|': '\u200D',  # input literal \| jadi ZWJ
    r'\\': '\u200C',  # input literal \\ jadi ZWNJ
}