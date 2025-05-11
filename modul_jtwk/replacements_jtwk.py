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
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ',
        'ai': 'ꜽ', 'au': 'ꜷ', 
        #'-' : ' ', 
        'Ç' : 'Ś', 'ç' : 'ś',
        '’' : '0‍',
        '‘' : '0‍',

        "x" : 'ś', "f" : 'ṣ', "t'" : 'ṭ', "d'" : 'ḍ', "q" : 'ĕ', "n`" : 'ñ', "n'" : 'ṇ', "o'" : 'ö',
        
        'v' : 'w',
        #'ṁ' : 'ŋ',
        'ṃ' : 'ŋ',  'ṁ' : 'ŋ',
        #'sh' : 'ś','ss' : 'ṣ',

        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ', 'Om̃' : 'Ōṃ',
    },
    'lampah': {
        'kh': 'ꝁ','gh': 'ǥ','ch': 'ꞓ','jh': 'ɉ',
        'ṭh': 'ṫ','ḍh': 'ḋ','th': 'ŧ','dh': 'đ',
        'ph': 'ꝑ','bh': 'ƀ','au': 'ꜷ','ai': 'ꜽ',
        '-' : ' ',
        '’' : '0‍',
        'v' : 'w',
        'ṁ' : 'ŋ',
        

        #'le': 'ḷ','ṛe': 'ṛ',

        'e' : 'è','E' : 'È', 'ê' : 'è', 'Ê' : 'È',#'sh' : 'ś','ss' : 'ṣ',
        'â':'ā', 'î':'ī', 
        'Ōm' : 'Ŏṃ','Ŏm' : 'Ōṃ','Ōm' : 'Ŏṃ',
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
replacements['modern_lampah'] = replacements['sriwedari'].copy()
#replacements['satya'] = replacements['sriwedari'].copy()

def replace_numbers_with_colon(text):
    text = re.sub(r'([\dA-Za-z]+[/\\][\dA-Za-z]+[/\\][\dA-Za-z]+)', r':\1:', text)
    return text


#versi yang stabil
import re

RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ]')
RE_KONSONAN = re.compile(r'[^aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ\s\u200C\u200D]')
ZWNJ = '\u200C'
VOWELS = 'aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOWEL_PENDEK = 'aiuĕAIUĔ'
VOWEL_PANJANG = 'āâîīûūêôeèéoöꜽꜷĀÂÎĪÛŪÊÔÉÈÖŌꜼꜶ'
KHUSUS_KONSONAN = 'ṅŋḥṙ'

def bersihkan_karakter_tak_terlihat(teks):
    return re.sub(r'[\u200C\u200D\s]', '', teks)

def get_clean_metrum(line):
    line = line.replace('-', '–')
    hasil = []
    def extract_metrum_segment(segment):
        return [c for c in segment if c in ['–', '⏑', '⏓']]
    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            blok = extract_metrum_segment(isi) * perkalian
            line_di_luar = line[:match.start()] + line[match.end():]
            luar = extract_metrum_segment(line_di_luar)
            return luar[:match.start()] + blok + luar[match.end():]
    return [c for c in line if c in ['–', '⏑', '⏓']]

def hitung_jumlah_metrum(line):
    if "[" in line and "]" in line:
        match = re.search(r'\[([–⏑⏓\s\u200C\u200D]*)][^\S\n]*×(\d+)', line)
        if match:
            isi = match.group(1)
            perkalian = int(match.group(2))
            isi_bersih = bersihkan_karakter_tak_terlihat(isi)
            jumlah_dalam_blok = sum(1 for _ in re.finditer(r'[–⏑⏓-]', isi_bersih))
            baris_di_luar = line[:match.start()] + line[match.end():]
            jumlah_di_luar = sum(1 for _ in RE_METRUM_SIMBOL.finditer(baris_di_luar))
            return (jumlah_dalam_blok * perkalian) + jumlah_di_luar
    return sum(1 for _ in RE_METRUM_SIMBOL.finditer(line))

def proses_puisi_buffer(puisi_buffer, current_metrum):
    if not current_metrum:
        return puisi_buffer
    processed = []
    panjang_metrum = len(current_metrum)
    for i, line in enumerate(puisi_buffer):
        selected_metrum = current_metrum[i % panjang_metrum]
        vokal_posisi = []
        idx_metrum = 0
        for idx, char in enumerate(line):
            if char.lower() in VOWELS and idx_metrum < len(selected_metrum):
                vokal_posisi.append((idx, char, selected_metrum[idx_metrum]))
                idx_metrum += 1
        hasil_line = list(line)
        i_vokal = 0
        while i_vokal < len(vokal_posisi) - 1:
            idx1, v1, met1 = vokal_posisi[i_vokal]
            idx2, v2, met2 = vokal_posisi[i_vokal + 1]
            v1_lower, v2_lower = v1.lower(), v2.lower()
            text_between = line[idx1 + 1:idx2]
            if re.fullmatch(r'[^\S\n]+', text_between):
                if met1 == '⏑' and met2 == '⏑':
                    if v1_lower in VOWEL_PENDEK and v2_lower in VOWEL_PENDEK:
                        hasil_line[idx2] = ZWNJ + v2.upper()
                        i_vokal += 2
                        continue
                elif v1_lower in VOWEL_PENDEK and v2_lower in VOWELS and met1 == '⏑' and met2 == '–':
                    hasil_line[idx2] = ZWNJ + v2.upper()
                    i_vokal += 2
                    continue
                elif v1_lower in VOWEL_PANJANG and v2_lower in VOWELS and met1 == '–' and met2 == '⏑':
                    hasil_line[idx2] = ZWNJ + v2.upper()
                    i_vokal += 2
                    continue
            elif met1 == '–' and v1_lower in VOWEL_PENDEK and ' ' in text_between:
                kata_kata = list(re.finditer(r'\S+', line))
                kata_list = [(m.start(), m.end(), m.group()) for m in kata_kata]
                kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                if kata_v1 and kata_v2 and kata_v1 != kata_v2:
                    if kata_v2[2][0] in VOWELS:
                        bagian_setelah_v1 = kata_v1[2][kata_v1[2].index(v1) + 1:]
                        konsonan_setelah_v1 = []
                        for char in bagian_setelah_v1:
                            if char in VOWELS:
                                break
                            if char not in ' \t\n\r\u200C\u200D' and RE_KONSONAN.search(char):
                                konsonan_setelah_v1.append(char)
                        if len(konsonan_setelah_v1) == 1:
                            konsonan = konsonan_setelah_v1[0]
                            if konsonan in KHUSUS_KONSONAN and v1_lower in VOWEL_PENDEK:
                                hasil_line[idx2] = ZWNJ + v2.upper()
                                i_vokal += 2
                                continue
                            elif konsonan not in KHUSUS_KONSONAN:
                                hasil_line[idx2] = ZWNJ + v2.upper()
                                i_vokal += 2
                                continue
            i_vokal += 1
        processed.append(''.join(hasil_line))
    return processed

def aplikasikan_metrum_dan_tandai_vokal(teks):
    blok_list = re.split(r'\n\s*\n', teks.strip(), flags=re.MULTILINE)
    hasil_blok = []
    current_metrum = []
    puisi_buffer = []
    for blok in blok_list:
        baris = blok.strip().splitlines()
        metrum_baris = [b for b in baris if RE_METRUM_SIMBOL.search(b) or (b.startswith("<") and ":" in b)]
        puisi_baris = [b for b in baris if not (RE_METRUM_SIMBOL.search(b) or (b.startswith("<") and ":" in b))]
        if metrum_baris:
            if puisi_buffer:
                processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                hasil_blok.append('\n'.join(processed))
                puisi_buffer = []
            current_metrum_temp = []
            for line in metrum_baris:
                if RE_METRUM_SIMBOL.search(line):
                    current_metrum_temp.append(get_clean_metrum(line))
            current_metrum = current_metrum_temp
            hasil_blok.append('\n'.join(metrum_baris))
        elif puisi_baris:
            puisi_buffer.extend(puisi_baris)
    if puisi_buffer:
        processed = proses_puisi_buffer(puisi_buffer, current_metrum)
        hasil_blok.append('\n'.join(processed))
    return '\n\n'.join(hasil_blok)

def tandai_vokal_pendek_dalam_pasangan(text):
    blok_list = re.split(r'\n\s*\n', text.strip(), flags=re.MULTILINE)
    hasil_blok = []
    current_metrum = []
    for blok in blok_list:
        puisi_buffer = []
        baris = blok.strip().splitlines()
        metrum_lines = []
        for line in baris:
            if line.startswith("<") and ":" in line:
                # Judul metrum ditemukan
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                if metrum_lines:
                    hasil_blok.extend(metrum_lines)
                    metrum_lines = []
                hasil_blok.append(line)
                current_metrum = []
            elif RE_METRUM_SIMBOL.search(line):
                # Baris simbol metrum
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                jumlah = hitung_jumlah_metrum(line)
                metrum_line = f"{line} : {jumlah}"
                metrum_lines.append(metrum_line)
                current_metrum.append(get_clean_metrum(line))
            else:
                # Baris puisi
                puisi_buffer.append(line)
        if metrum_lines:
            hasil_blok.extend(metrum_lines)
        if puisi_buffer:
            processed = proses_puisi_buffer(puisi_buffer, current_metrum)
            hasil_blok.extend(processed)
        hasil_blok.append("")
    hasil_akhir = "\n".join(hasil_blok).strip()
    return hasil_akhir