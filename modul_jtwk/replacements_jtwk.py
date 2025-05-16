import re

# Set transliterasi untuk berbagai mode
replacements = {
    'kinanti': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        'ᶇ': 'ŋ', 'ᶆ': 'ṃ', 'ꞕ': 'ḥ', 'ᶉ': 'ṙ', 
        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'ĕ','E' : 'Ĕ','sh' : 'ś','ss' : 'ṣ',
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
    'normal': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'ĕ','E' : 'Ĕ','sh' : 'ś','ss' : 'ṣ',
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
        'kakawin': {
        'ng': 'ṅ',
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'th': 'ŧ','ṭh': 'ṫ','ḍh': 'ḋ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ',
        'ai': 'ꜽ', 'au': 'ꜷ', 
        #'-' : ' ', 
        'Ç' : 'Ś', 'ç' : 'ś',
        '’' : '0‍',
        '‘' : '0‍',

        "x" : 'ś', "f" : 'ṣ', "t'" : 'ṭ', "d'" : 'ḍ', "q" : 'ĕ', "n`" : 'ñ', "n'" : 'ṇ', "o'" : 'ö', 'v' : 'w',
        #'ṃ' : 'ŋ',  
        'ṁ' : 'ŋ',
        #'sh' : 'ś','ss' : 'ṣ',

        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ', 'Om̃' : 'Ōṃ',
    },
    'jawa': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'ĕ','E' : 'Ĕ','sh' : 'ś','ss' : 'ṣ',
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
    },
    'pali': {
        'E': 'È',  # Pali specific replacement
        'e': 'è',  # Pali specific replacement
        'kh': 'ꝁ', 'gh': 'ǥ', 'ch': 'ꞓ', 'jh': 'ɉ',
        'ṭh': 'ṭ', 'ḍh': 'ḋ', 'th': 'ŧ', 'dh': 'đ',
        'ph': 'ꝑ', 'bh': 'ƀ', 'ḷi': 'ḹ', ';': ':',
    },
    'sastra_org': {
        'kh': 'ꝁ', 'gh': 'ǥ',
        'ch': 'ꞓ', 'jh': 'ɉ',
        'th': 'ṭ', 'dh': 'ḍ',
        'ph': 'ꝑ', 'bh': 'ƀ',

        'ê' : 'ĕ', 'Ê' : 'Ĕ',
        'e' : 'è', 'E': 'È',
        'le': 'ḷ', 'ṛe': 'ṛ', 'ia' : 'y',
    },
    'sriwedari': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'ḍ',
        'ph': 'ꝑ','bh': 'ƀ', 'ny': 'ñ', 'iè': 'iyè',

        'ê' : 'ĕ', 'Ê' : 'Ĕ',
        'e' : 'ĕ', 'E': 'Ĕ',
        'é' : 'è', 'É' : 'È', 
        'le': 'ḷ', 'ṛe': 'ṛ', 'ia' : 'ya',
    },
    'satya': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ṭ','dh': 'ḍ',
        'ph': 'ꝑ','bh': 'ƀ', 'ny': 'ñ', 'iè': 'iyè',

        'ê' : 'ĕ', 'Ê' : 'Ĕ',
        'e' : 'è', 'E': 'Ĕ',
        #'é' : 'è', 'É' : 'È', 
        'le': 'ḷ', 'ṛe': 'ṛ', 'ia' : 'ya',
        '-': '',
    },
    'cerita': {
        'kh': 'ḳ', 'ua' : 'wa', 'ia' : 'ya',
        'gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ', 'ny' : 'ñ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ṭ','dh': 'ḍ',
        'ph': 'ꝑ','bh': 'ƀ', #'ny': 'ñ',

        'e' : 'ĕ','E' : 'Ĕ',
    },
        'sanskrit': {
        #'E': 'È',  # Pali specific replacement
        'e': 'è',  # Pali specific replacement
        'kh': 'ꝁ', 'gh': 'ǥ', 'ch': 'ꞓ', 'jh': 'ɉ',
        'ṭh': 'ṭ', 'ḍh': 'ḋ', 'th': 'ŧ', 'dh': 'đ',
        'ph': 'ꝑ', 'bh': 'ƀ', 'ḷi': 'ḹ', 
        'v': 'w', 'ai' : 'ꜽ', 'au' : 'ꜷ', 'oṃ':'Ōṃ', 'Oṁ':'Ōṃ', 'Om̃':'Ōṃ',
        "'" : "0", "’" : "0", 'ṃ' : 'ŋ', 'ṁ' : 'ŋ'
    }
}

# Mode kakawin mewarisi mode normal dan menambahkan/menimpa beberapa entri
#replacements['lampah'] = replacements['kakawin'].copy()
replacements['lampah'] = replacements['kakawin'].copy()
#replacements['satya'] = replacements['sriwedari'].copy()

def replace_numbers_with_colon(text):
    text = re.sub(r'([\dA-Za-z]+[/\\][\dA-Za-z]+[/\\][\dA-Za-z]+)', r':\1:', text)
    return text

