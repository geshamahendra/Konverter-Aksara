from modul_jtwk.konstanta import DAFTAR_VOKAL, DAFTAR_KONSONAN, SH, VOKAL_PANJANG

kamus_filter = {
    #Aksara Suci
    'Ai': 'Ꜽ', 'Au': 'Ꜷ', r'(\*|\#)[Oo]m': r'\1Ōṃ',
    'ai': 'ꜽ', 'au': 'ꜷ', 
    'ng': 'ṅ', r'\b^h' : 'ʰ',

    #Pembalik layar-mahaprana
    rf'[rṙᶉ]([{DAFTAR_KONSONAN.replace("t","").replace("w","").replace("ś","")}])\1': r'r\1', 
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
    
    #en dash khusus
    r'(rĕs)(?: |-)(?=rĕs)': r'\1–',

    r'\bsa[ṅn]k[sṣ][eèé]pa': 'saŋkṣepa',
    rf'\bsa[nṅ](s|ṣ)ipt([{DAFTAR_VOKAL}])': r'saŋ\1ipt\2',
    r'\bsa[n|ṅ]ṣipta': 'saŋṣ',
    r'ṅkt': 'ŋkt', r'ṅ[ṣs][ṭt]r': 'ŋṣṭr', rf'ṅsk': r'ŋsk',

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
    #intra-kata
    r'(?:\b(m|p)aṅr|(\w+)āṅr|(\w+)âṅr)(\w+)': lambda m: (
        (m.group(1) or m.group(2) or m.group(3))
        + ('aŋ' if m.group(1) else 'āŋ')
        + 'r' + m.group(4)
        if sum(c in DAFTAR_VOKAL for c in m.group(4)) >= 2 else m.group(0)
    ),
    #antar-kata
    rf'([{DAFTAR_KONSONAN}])[^\S\n]+aṅr(\w+)': lambda m: (
        m.group(1) + 'aŋr' + m.group(2)
        if sum(c in DAFTAR_VOKAL for c in m.group(2)) >= 2 else m.group(0)
    ),

    # Imbuhan aṅrw / āṅrw[aā]
    #intra-kata
    r'(?:\b(m|p)aṅrw|(\w+)āṅrw|(\w+)âṅrw)(a|ā)': lambda m: (
        (m.group(1) or m.group(2) or m.group(3))
        + ('aŋ' if m.group(1) else 'āŋ')
        + 'rw' + m.group(4)
    ),
    #antar-kata
    rf'([{DAFTAR_KONSONAN}])[^\S\n]+aṅrw(a|ā)': lambda m: (
        m.group(1) + 'aŋrw' + m.group(2)
    ),
    
    # Imbuhan aṅrĕ
    #intra-kata
    r'(?:\b(m|p)aṅrĕ|(\w+)āṅrĕ|(\w+)âṅrĕ)(e|ĕ)': lambda m: (
        (m.group(1) or m.group(2) or m.group(3))
        + ('aŋ' if m.group(1) else 'āŋ')
        + f'{SH}rĕ' + m.group(4)
    ),
    #antar-kata
        rf'([{DAFTAR_KONSONAN}])[^\S\n]+aṅrĕ(e|ĕ)': lambda m: (
        m.group(1) + f'aŋ{SH}rĕ' + m.group(2)
    ),

    # Imbuhan aṅ lainnya (selain g/k)
    #intra-kata
    rf'(?:\b(m|p)aṅ|(\w+)āṅ|(\w+)âṅ)((?![gk])[{DAFTAR_KONSONAN}])(\w+)': (
        lambda m: (
            (m.group(1) or m.group(2) or m.group(3))
            + ('aŋ' if m.group(1) else 'āŋ')
            + m.group(4) + m.group(5)
            if sum(c in DAFTAR_VOKAL for c in m.group(5)) >= 2
            else m.group(0)
        )
    ),
    #antar-kata
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
    r'(\w)([āâ])ṅ(jrah)\b': r'\1\2ŋ\3',

    #an khusus
    r'an jrih': r'añ jrih',
    r' n ton': r' nton',
    
    #mār khusus
    r'm[āa]r(b[ua])': r'mār\\\1',

    #pemisah kata ulang
    r'\b([A-Za-z]{2,}?)(?=(?!–)\1\b)' : r'\1-',# kecualikan en dash
    #kembalikan kata ulang
    r'\b(sum)-\1': r'\1\1',

    #akhiran khusus
    r'ṅ(ni|nira|nire|nik)(ṅ?)\b': r'ŋ\1\2',
    r'h(ni|nira|nire|nik)(ṅ?)\b': r'ḥ\1\2',
    r'r(ni|nira|nire|nik)(ṅ?)\b': r'r\\\1\2',

    #rf'\bm([āa])r([{DAFTAR_KONSONAN.replace("y","").replace("w",#"").replace("s","")}])(\w+)(?![{DAFTAR_KONSONAN}])':
    #lambda m: (
    #    f"mār\\{m.group(2)}{m.group(3)}"
    #    if sum(c in DAFTAR_VOKAL for c in m.group(3)) >= 2
    #    else m.group(0)
    #),

}