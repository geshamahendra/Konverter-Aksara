from modul_jtwk.konstanta import DAFTAR_VOKAL, DAFTAR_KONSONAN, SH, VOKAL_PANJANG

kamus_inti = {
    
    
    #aturan baku
    r'lĕṅlĕṅ':'lĕŋlĕŋ', r'nuṅ(s|t)uṅ':r'nuŋ\1uṅ',
    r'rĕṅrĕṅ':'rĕŋrĕṅ',
    
    #suku kata khusus
    #rf'\b([{DAFTAR_KONSONAN}]+)a([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ā\2',
    #rf'\b([{DAFTAR_KONSONAN}]+)i([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ī\2',
    #rf'\b([{DAFTAR_KONSONAN}]+)u([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ū\2',
    #rf'\b([{DAFTAR_KONSONAN}]+)ĕ([{DAFTAR_KONSONAN}]+[^\S\n]+[{DAFTAR_KONSONAN}])': r'\1ö\2',

    #Kasus khusus
    r'duh(k|ꝁ)(ita|[' + DAFTAR_VOKAL + '])' : r'duḥꝁ\2', #duhka duhkita
    r'rwarw(a|ā|â)' : r'rwa-rw\1', # rwa rwa
    r'\b(p|m)?aṅlĕ' : r'\1aŋlĕ', r'(\w)āṅlĕ' : r'\1āŋlĕ',
    r'(ā|a|â)ḥniṅ\b' : r'\1hniṅ',
    r'\bmasku\b' : r'māsku',
    r'[ꜽe]rtal([iy])' : r'ꜽr\\tal\1',

    #=================#

    #pemanjang vokal suku kata tunggal diapit konsonan
    #rf'\b([{DAFTAR_KONSONAN}])a([{DAFTAR_KONSONAN}]\s*[{DAFTAR_KONSONAN}])': r'\1ā\2',
    #rf'\b([{DAFTAR_KONSONAN}])i([{DAFTAR_KONSONAN}]\s*[{DAFTAR_KONSONAN}])': r'\1ī\2',
    #rf'\b([{DAFTAR_KONSONAN}])u([{DAFTAR_KONSONAN}]\s*[{DAFTAR_KONSONAN}])': r'\1ū\2',

    #=============================
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
    r'\bky[aā]t[iī]\b': 'ꝁyāti', r'\bky[aā]t(iī)(\w)': r'ꝁyāt\1\2', 
    r'[aāâ]pt([iy])': r'āpt\1',

    r'\bkar[ĕe]na': 'karĕṇa', r'\bwau\b': 'wawu',
    r'\bwong\b': 'wwoṅ', r'\bṅka': 'ṅkā', 
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
    r'([pc])urna': r'\1ūrna', r'hidĕp': 'hiḍĕp', r'rĕsi':'rĕṣi', 
    r'purwa': 'pūrwa', 
    r'murt(t)?([iy])': r'mūrtt\2',
    r'kirt(t)?([iy])': r'kīrtt\2', 
    r'prapta': 'prāpta',
    r't[iī]k[sṣ][nṇ]': 'tīkṣṇ',
    r'\b(mu|minu)[sṣ][tṭ]i': r'\1ṣṭi', 
    r'naŧa': 'nāŧa',
    r'prabu': 'praƀu', r'gun(a|ā)': r'guṇ\1', 
    r'\bmèga\b': 'mèǥa', r'\brat\b': 'rāt',
    r'g[āa][ṇn][dḍ]ew': 'gāṇḍew',
    r'\bbra\b': 'ƀra', r'\b[bƀ]a[tŧṭ]ar': 'ƀaṭār', r'\bs[aā]mpun\b': 'sampun', r'wakpatu': 'wākpaṭu', 
    r'\bwirya': 'wīrya', r'wisa': 'wiṣa', #r'\brasa\b': 'raṣa', 
    r'uksma': 'ūkṣma', 
    r'\bmaha(?!ntĕn)': 'mahā', 
    r'\bmahar[sṣ]i': 'mahāṙṣi',

    r'\b[ƀb][aā][sṣ]a': 'ƀaṣa',
    
    r'\bi[sś]wara': 'iśwara', 
    r'r[aā][sṣś]mi': 'raśmi',
    r'r[aā]mya': 'ramya', r'[sś]iǥra': 'śīǥra', r's[aā]k[sṣ][aā]t': 'sākṣāt', r'maṅsa': 'māṅsa',
    r'[dḍ]at[ĕe]ṅ': 'ḍatĕṅ', r'ratri': 'rātri', 
    r'm(u|e)sti\b': r'm\1ṣṭi',
    r'hid(ĕ|e)p': 'hiḍĕp', r'yogi[sś]wara': 'yogīśwara', r'dusta': 'duṣṭa', r'makuta': 'makuṭa', r'man(i|ī|y)': r'maṇ\1',  r'\bsirna\b': 'śīrna', r'\b[sś]ar[iī]ra': 'śarīra', r'atma': 'ātma', 
    r'pranata': 'praṇata',  
    r'sꝑatik': 'sꝑaṭik',
    r'ǥosa': 'ǥoṣa', 
    r'k(a|ā)r(a|ā)na': r'k\1r\2ṇa',  r'patni': 'patnī', r'drĕ[ḍđ]a': 'drĕḋa', r'saṅkya': 'saṅꝁya', r'bakti': 'ƀakti', r'nipuna': 'nipuṇa', r'ƀarana': 'ƀaraṇa', r'ka[tṭ][uū][nṅ]ka': 'kaṭuṅka',
    r'(?<!~)\brana\b': 'raṇa', 
    r'\bwana\b': 'waṇa',
    
    r'(?<!ga)gana\b': r'gaṇa', r'\bgana\b': r'gaṇa',
    r'raksasa': 'rākṣasa', r'samānta': r'samanta',
    r'r[aā]ksa(\w?)\b': r'rakṣa\1', r'kĕdap': 'kĕḍap',
    r'k([ou])t([iy])': r'k\1ṭ\2', r'paramarŧa': 'paramārŧa',
    
    r'\bb([aā])na': r'b\1ṇa',
    r'osad': 'oṣad', r'bhagya': 'bhāgya',
    r'ƀaskar': 'ƀaṣkar', r'dĕp': 'ḍĕp', r'k[aā]n[tṭ]a\b': 'kaṇṭa', r'br[aā]hm': 'brahm',
    r'brahmana': 'brahmaṇa', 
    
    r'\byasa\b': 'yaśa', r'esti\b': 'eṣṭi', 
    
    r'pudak': 'puḍak', r'aṅin(\s?)dar[aā]t': 'aṅiṇḍarat', r'darat': 'ḍarat', r'([tn])unda': r'\1unḍa', r'kinanta': 'kinanṭa',
    r'g[eĕ][nṇ][dḍ]iṅ': 'gĕṇḍiṅ', r'duduk': 'ḍuḍuk', r'li[nṇ][dḍ](u|ū|w)': r'linḍ\1', r't[eĕ][dḍ][uū]([n])': r'tĕḍu\1',  
    r'tum[eĕ][dḍ][uū]([n])': r'tumĕḍu\1',
    r'padaṅ': 'paḍaṅ', r'tindih': 'tinḍih', r'dukuh': 'ḍukuh', r'undu([tk])': r'unḍu\1', r'ĕdap\b': r'ĕḍap', 
    r'd([aā])nd([āa])': r'ḍanḍ\1', r'garuda': 'garuḍa', r'tadah': 'taḍah', r'p[āa]n[dḍ]aw': 'pānḍaw', r'p[āa]n[dḍ]u': 'pānḍu', 
    r'tĕndas': 'tĕnḍas', r'mandala': 'manḍala', r'gandewa': 'ganḍewa', r'manda\b': 'manḍa', r'tanda': 'tanḍa',

    r'([sn])[eĕ][dḍ][eĕ]ṅ\b': r'\1ĕḍĕṅ',
    r'ndĕ([ms])': r'nḍĕ\1',
    r'dĕdĕt': r'ḍĕḍĕt',
    
    r'\brasmi': 'raṣmi', 
    r'r[aā]tn[aā]' : 'ratna', r'ratnakand': r'ratnakanḍ',
    r'\bsaj(ñ|n)[aā]': 'sajñā', r'pra[bƀ][aā]wa': 'praƀāwa', r'\bk[aā][sś]mala': 'kaśmala', 
    
    r'g(ĕ|a)d(a|u|i)ṅ': r'g\1ḍ\2ṅ', 
    r'p(i|u)nd(a|u)': r'p\1nḍ\2',
    r'pininda': r'pininḍa', r'(ta|sa)[nṇ]diṅ': r'\1ṇḍiṅ', r'pandan': r'panḍan', r'gundik': r'gunḍik', r'k[eĕ]ndaṅ': r'kĕnḍaṅ', 

    #pendekkan
    r'āścāry': 'āścary', 
    r'\bs[aā]smrĕti': 'sasmrĕti',  r'c[iī]tta': 'citta',
    r'([pd])āksa': r'\1aksa', 
    r'wākt(r?)a': r'wakt\1a', r'\b[sś][uū]kl': 'śukl',  
    r'māntuk': 'mantuk', 
    r'd[iī](b|w)ya': r'di\1ya', 
    r'[ƀb][uū]kt([iy])': r'ƀukt\1',
    r'b[aā]y([uw])': r'bāy\1',
    r's[aā]nma[tŧ]a': 'sanmata',  r'ma[nṇ][iī]ndr': 'maṇīndr', 
    r'k[aā]sturi': 'kasturi', r'wiwāk[sṣ]a': 'wiwaksa', r'wārga': 'warga', r'parātra': 'paratra', 
    r'[sṣś]aktim[aā]nt': 'śaktimant',

    r'dūrga': 'durga', r'rūdr': 'rudr',
    r'pr[aā]l[aā]m[bƀ]': 'pralamb', 
    r'pr[aā]k[aā]mp': 'prakamp',
    r'm[aā][nṇ][dḍ][eĕ]g': 'maṇḍĕg', 

    #konsonan ganda
    r'm[aā]rtyaloka': 'marttyaloka', r't[aā]twa': 'tattwa', r'jag[aā]ttraya': 'jagattraya', 

    rf'b[aā][hḥ]n([{DAFTAR_VOKAL}]|y)': r'bahn\1',
    rf'\b(m|p)āt([{DAFTAR_VOKAL}]|y)': r'\1at\2',  
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
    rf'w([ie])sn([{DAFTAR_VOKAL}]|w)': r'w\1ṣṇ\2',
    rf'p([ou])rus([{DAFTAR_VOKAL}])': r'p\1ruṣ\2',
    rf'k(a|ā)ra[nṇ]([{DAFTAR_VOKAL}])': r'k\1raṇ\2',
    rf'muky([{DAFTAR_VOKAL}])': r'muꝁy\1',
    rf'pa[dḍ]([{DAFTAR_VOKAL}])(?!dway)': r'paḍ\1',
    rf'pram([aā])n([{DAFTAR_VOKAL}])': r'pram\1ṇ\2',
    rf'k[sṣ]a[ṇn]([{DAFTAR_VOKAL}])': r'kṣaṇ\1',
    rf'sury([{DAFTAR_VOKAL}])': r'sūry\1',
    rf'm[aā]rg([{DAFTAR_VOKAL}])(?!lawu)': r'mārg\1',
    rf'(?<!u)(?<!kahawa)(?<!krū)(?<![{DAFTAR_KONSONAN}][{DAFTAR_KONSONAN}])r([{DAFTAR_VOKAL.replace("ā","")}])n([{DAFTAR_VOKAL.replace("ĕ","")}])': r'r\1ṇ\2',
    rf'(?<! [{DAFTAR_VOKAL}][{DAFTAR_KONSONAN}][{DAFTAR_VOKAL}])(?<![{DAFTAR_KONSONAN}][{VOKAL_PANJANG}])muk([{DAFTAR_VOKAL}])': r'muꝁ\1',
    rf'[ṣsś][iī]rn([{DAFTAR_VOKAL}])': r'śīrn\1', 
    rf'k[iī]rn([{DAFTAR_VOKAL}])': r'kīrn\1', 

    #bisa merubah wirama
    r'ṅuni': 'ṅūni', r'\brah' : 'rāh',
    r'nagara': 'nāgara', r'pat\b': 'pāt',
    r'\bsad': 'ṣaḍ',
    r'\brum': 'rūm', r'tut(?![iy])': 'tūt', r'tinut': 'tinūt',
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
    #bunyi a
    r'\b([āâ])(kra|kweh|rđ|ṅlih|gya|mbĕk|[sś]ray|psara|mrĕta|mrih|ntara|stra|gra|hyun|ntaka|glis|sraṅ|sya|ksi|ṅhiṅ|hya|ṅga|ntĕn|dƀut|gny)': r'a\1', 
    
    rf'(?<!^nir)(?<! aṅ)(?<! [{DAFTAR_KONSONAN}])(?<![{DAFTAR_KONSONAN}]y)(?<![{DAFTAR_KONSONAN}]w)(?<!\snir)(?<!\saw)(?<!^s)(?<!\ss)(?<!\s)(?<!<)(?<!\{{)a(kra|kweh|rđ|ṅlih|gya|mbĕk|psara|mrĕta|mrih|ntara|stra|gra|hyun|ntaka|glis|sraṅ|sya|ksi|ṅhiṅ|gni|hya|ṅga|ntĕn|dƀut|gny)': r'ā\1',

    #bunyi i
    r'\b[iī](ndr)': r'i\1', 
    rf'(?<!nir)(?<!<)(?<!\{{)(?<!\s)[iī](ndr)': r'ī\1',

    #backsplash buat pemutus
    r'\\\|': '\u200D',  # input literal \| jadi ZWJ
    r'\\': '\u200C',  # input literal \\ jadi ZWNJ
}