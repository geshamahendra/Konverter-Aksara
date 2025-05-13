
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
    """
    Membersihkan karakter tak terlihat (zero-width non-joiner, spasi) dari teks.

    Args:
        teks (str): Teks yang akan dibersihkan.

    Returns:
        str: Teks yang sudah dibersihkan.
    """
    return re.sub(r'[\u200C\u200D\s]', '', teks)

def get_clean_metrum(line):
    """
    Mengekstrak simbol-simbol metrum dari sebuah baris teks.  Menangani pengulangan metrum.

    Args:
        line (str): Baris teks yang mengandung simbol metrum.

    Returns:
        list: List berisi simbol-simbol metrum ('–', '⏑', '⏓').
    """
    line = line.replace('-', '–') #normalisasi
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
    """
    Menghitung jumlah simbol metrum dalam sebuah baris teks, termasuk yang ada dalam pengulangan.

    Args:
        line (str): Baris teks yang mengandung simbol metrum.

    Returns:
        int: Jumlah simbol metrum.
    """
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
    """
    Menerapkan metrum pada baris-baris puisi dalam buffer.

    Args:
        puisi_buffer (list): List berisi baris-baris puisi yang akan diproses.
        current_metrum (list): List berisi simbol-simbol metrum yang akan diterapkan.

    Returns:
        list: List berisi baris-baris puisi yang sudah diproses.
    """
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
                            if len(konsonan_setelah_v1) == 1 and v1_lower in VOWEL_PENDEK:
                                hasil_line[idx2] = ZWNJ + v2.upper()
                                i_vokal += 2
                                continue
            # Logika pemanjangan vokal yang diperbaiki
            if i_vokal < len(vokal_posisi):
                idx_vokal, vokal, metrum_vokal = vokal_posisi[i_vokal]
                vokal_lower = vokal.lower()
                if vokal_lower in 'aiu' and metrum_vokal == '–':
                    next1_idx = idx_vokal + 1
                    next2_idx = idx_vokal + 2
                    if next2_idx < len(line):
                        char1 = line[next1_idx]
                        char2 = line[next2_idx]
                        if RE_KONSONAN.match(char1) and RE_VOKAL.match(char2):
                            if vokal_lower == 'a':
                                hasil_line[idx_vokal] = 'ā'
                            elif vokal_lower == 'i':
                                hasil_line[idx_vokal] = 'ī'
                            elif vokal_lower == 'u':
                                hasil_line[idx_vokal] = 'ū'
            i_vokal += 1
        processed.append(''.join(hasil_line))
    return processed



def aplikasikan_metrum_dan_tandai_vokal(teks):
    """
    Fungsi utama untuk mengaplikasikan metrum dan menandai vokal pada teks puisi.
    Fungsi ini memproses teks per blok, mengenali blok metrum dan blok bait,
    serta menerapkan aturan metrum yang sesuai.

    Args:
        teks (str): Teks puisi yang akan diproses. Teks diharapkan memiliki format
                    blok metrum dan blok bait yang dipisahkan oleh baris kosong.

    Returns:
        str: Teks puisi yang sudah diproses, dengan penerapan metrum dan penandaan vokal.
    """
    blok_list = re.split(r'\n\s*\n', teks.strip(), flags=re.MULTILINE)
    hasil_blok = []
    current_metrum = []

    for blok in blok_list:
        baris = blok.strip().splitlines()
        is_metrum_blok = any(RE_METRUM_SIMBOL.search(b) for b in baris)
        header_blok = [b for b in baris if (b.startswith("<") and ":" in b) or (b.startswith("{") and ":" in b)]
        puisi_baris = [b for b in baris if not RE_METRUM_SIMBOL.search(b) and not (b.startswith("<") and ":" in b)]
        metrum_baris_temp = [get_clean_metrum(b) for b in baris if RE_METRUM_SIMBOL.search(b)]

        hasil_blok.extend(header_blok)

        if is_metrum_blok:
            current_metrum = metrum_baris_temp
            hasil_blok.extend(baris) # Sertakan kembali baris metrum dalam output
        elif current_metrum:
            jumlah_metrum = len(current_metrum)
            processed_puisi = []
            if jumlah_metrum == 1:
                for line in puisi_baris:
                    processed_puisi.extend(proses_puisi_buffer([line], current_metrum))
            elif jumlah_metrum == 2:
                for i, line in enumerate(puisi_baris):
                    metrum_index = 0 if i % 2 == 0 else 1
                    processed_puisi.extend(proses_puisi_buffer([line], [current_metrum[metrum_index]]))
            elif jumlah_metrum >= 3:
                for i, line in enumerate(puisi_baris):
                    metrum_index = i % 3
                    processed_puisi.extend(proses_puisi_buffer([line], [current_metrum[metrum_index]]))
            else:
                processed_puisi = puisi_baris

            hasil_blok.extend(processed_puisi)
        else:
            hasil_blok.extend(puisi_baris) # Jika ini blok bait pertama dan belum ada metrum

        hasil_blok.append("") # Tambahkan baris kosong antar blok

    return "\n".join(hasil_blok).strip()

def tandai_vokal_pendek_dalam_pasangan(text):
    """
    Fungsi ini memproses teks puisi untuk menandai vokal pendek yang berada dalam
    pasangan dengan vokal pendek lainnya dalam satu kata, sesuai dengan aturan metrum.
    Fungsi ini juga menghitung jumlah metrum pada baris metrum.

    Args:
        text (str): Teks puisi yang akan diproses.

    Returns:
        str: Teks puisi yang sudah diproses, dengan vokal pendek yang ditandai
             dan jumlah metrum pada baris metrum.
    """
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

'''
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
                            if len(konsonan_setelah_v1) == 1 and v1_lower in VOWEL_PENDEK:
                                hasil_line[idx2] = ZWNJ + v2.upper()
                                i_vokal += 2
                                continue
            # Logika pemanjangan vokal yang diperbaiki
            if i_vokal < len(vokal_posisi):
                idx_vokal, vokal, metrum_vokal = vokal_posisi[i_vokal]
                vokal_lower = vokal.lower()
                if vokal_lower in 'aiu' and metrum_vokal == '–':
                    next1_idx = idx_vokal + 1
                    next2_idx = idx_vokal + 2
                    if next2_idx < len(line):
                        char1 = line[next1_idx]
                        char2 = line[next2_idx]
                        if RE_KONSONAN.match(char1) and RE_VOKAL.match(char2):
                            if vokal_lower == 'a':
                                hasil_line[idx_vokal] = 'ā'
                            elif vokal_lower == 'i':
                                hasil_line[idx_vokal] = 'ī'
                            elif vokal_lower == 'u':
                                hasil_line[idx_vokal] = 'ū'
            i_vokal += 1
        processed.append(''.join(hasil_line))
    return processed

def aplikasikan_metrum_dan_tandai_vokal(teks):
    blok_list = re.split(r'\n\s*\n', teks.strip(), flags=re.MULTILINE)
    hasil_blok = []
    current_metrum = []

    for blok in blok_list:
        baris = blok.strip().splitlines()
        is_metrum_blok = any(RE_METRUM_SIMBOL.search(b) for b in baris)
        header_blok = [b for b in baris if (b.startswith("<") and ":" in b)]
        puisi_baris = [b for b in baris if not RE_METRUM_SIMBOL.search(b) and not (b.startswith("<") and ":" in b)]
        metrum_baris_temp = [get_clean_metrum(b) for b in baris if RE_METRUM_SIMBOL.search(b)]

        hasil_blok.extend(header_blok)

        if is_metrum_blok:
            current_metrum = metrum_baris_temp
            hasil_blok.extend(baris) # Sertakan kembali baris metrum dalam output
        elif current_metrum:
            jumlah_metrum = len(current_metrum)
            processed_puisi = []
            if jumlah_metrum == 1:
                for line in puisi_baris:
                    processed_puisi.extend(proses_puisi_buffer([line], current_metrum))
            elif jumlah_metrum == 2:
                for i, line in enumerate(puisi_baris):
                    metrum_index = 0 if i % 2 == 0 else 1
                    processed_puisi.extend(proses_puisi_buffer([line], [current_metrum[metrum_index]]))
            elif jumlah_metrum >= 3:
                for i, line in enumerate(puisi_baris):
                    metrum_index = i % 3
                    processed_puisi.extend(proses_puisi_buffer([line], [current_metrum[metrum_index]]))
            else:
                processed_puisi = puisi_baris

            hasil_blok.extend(processed_puisi)
        else:
            hasil_blok.extend(puisi_baris) # Jika ini blok bait pertama dan belum ada metrum

        hasil_blok.append("") # Tambahkan baris kosong antar blok

    return "\n".join(hasil_blok).strip()

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
'''

'''
def proses_puisi_buffer(puisi_buffer, current_metrum):
    if not current_metrum:
        return puisi_buffer
    
    processed = []
    panjang_metrum = len(current_metrum)
    
    for i, line in enumerate(puisi_buffer):
        # Pilih metrum yang sesuai untuk baris ini
        metrum_index = i % panjang_metrum
        selected_metrum = current_metrum[metrum_index]
        
        # Penting: cetak metrum yang digunakan untuk debugging
        # print(f"Baris puisi: {line}")
        # print(f"Menggunakan metrum index {metrum_index}: {selected_metrum}")
        
        vokal_posisi = []
        idx_metrum = 0
        
        # Identifikasi posisi vokal dan metrum yang sesuai
        for idx, char in enumerate(line):
            if char.lower() in VOWELS and idx_metrum < len(selected_metrum):
                vokal_posisi.append((idx, char, selected_metrum[idx_metrum]))
                idx_metrum += 1
        
        hasil_line = list(line)
        i_vokal = 0
        
        # Proses vokal sesuai metrum
        while i_vokal < len(vokal_posisi) - 1:
            idx1, v1, met1 = vokal_posisi[i_vokal]
            idx2, v2, met2 = vokal_posisi[i_vokal + 1]
            v1_lower, v2_lower = v1.lower(), v2.lower()
            text_between = line[idx1 + 1:idx2]
            
            # Tangani kasus spesifik
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
                            if len(konsonan_setelah_v1) == 1 and v1_lower in VOWEL_PENDEK:
                                hasil_line[idx2] = ZWNJ + v2.upper()
                                i_vokal += 2
                                continue
            
            # PERBAIKAN: Logika pemanjangan vokal - dengan kondisi tambahan:
            # Hanya berlaku pada pola: konsonan + vokal_saat_ini + satu_konsonan + vokal_lain
            
            # Periksa apakah vokal ini berada dalam pola yang tepat
            valid_pattern = False
            
            # Cek apakah ada konsonan sebelum vokal ini
            prev_char_idx = idx1 - 1
            has_prev_consonant = False
            if prev_char_idx >= 0 and RE_KONSONAN.match(line[prev_char_idx]):
                has_prev_consonant = True
            
            # Cek apakah diikuti oleh satu konsonan diikuti vokal
            next_consonant_and_vowel = False
            if i_vokal < len(vokal_posisi) - 1:
                next_vowel_idx = vokal_posisi[i_vokal + 1][0]
                between_text = line[idx1 + 1:next_vowel_idx]
                # Jika hanya terdapat satu konsonan antara vokal ini dan vokal berikutnya
                # dan tidak ada spasi di antaranya
                if (' ' not in between_text and 
                    sum(1 for c in between_text if RE_KONSONAN.match(c)) == 1):
                    next_consonant_and_vowel = True
            
            # Pola valid jika kedua kondisi terpenuhi
            valid_pattern = has_prev_consonant and next_consonant_and_vowel
            
            # Logika pemanjangan vokal - hanya jika pola valid
            if v1_lower in 'aiu' and met1 == '–' and v1_lower not in VOWEL_PANJANG and valid_pattern:
                if v1_lower == 'a':
                    hasil_line[idx1] = 'ā'
                elif v1_lower == 'i':
                    hasil_line[idx1] = 'ī'
                elif v1_lower == 'u':
                    hasil_line[idx1] = 'ū'
            
            # Sebaliknya, pastikan vokal pendek jika metrumnya pendek - juga hanya jika pola valid
            elif v1_lower in 'āīū' and met1 == '⏑' and valid_pattern:
                if v1_lower == 'ā':
                    hasil_line[idx1] = 'a'
                elif v1_lower == 'ī':
                    hasil_line[idx1] = 'i'
                elif v1_lower == 'ū':
                    hasil_line[idx1] = 'u'
            
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

def debug_metrum_pada_puisi(puisi_text):
    lines = puisi_text.strip().splitlines()
    
    # Cari baris metrum
    metrum_lines = []
    for line in lines:
        if RE_METRUM_SIMBOL.search(line):
            metrum_lines.append(get_clean_metrum(line))
    
    if not metrum_lines:
        return "Tidak ditemukan baris metrum"
    
    # Identifikasi baris puisi
    puisi_lines = [line for line in lines if not RE_METRUM_SIMBOL.search(line) and not (line.startswith("<") and ":" in line)]
    
    hasil = []
    for i, puisi in enumerate(puisi_lines):
        metrum_idx = i % len(metrum_lines)
        metrum = metrum_lines[metrum_idx]
        
        hasil.append(f"Baris puisi: {puisi}")
        hasil.append(f"Metrum: {''.join(metrum)}")
        
        # Identifikasi vokal
        vokal_posisi = []
        idx_metrum = 0
        for idx, char in enumerate(puisi):
            if char.lower() in VOWELS and idx_metrum < len(metrum):
                vokal_posisi.append((idx, char, metrum[idx_metrum]))
                idx_metrum += 1
        
        # Tampilkan vokal dengan metrum
        vokal_debug = []
        for idx, char, met in vokal_posisi:
            # Cek pola: konsonan + vokal_saat_ini + satu_konsonan + vokal_lain
            valid_pattern = False
            
            # Cek apakah ada konsonan sebelum vokal ini
            prev_char_idx = idx - 1
            has_prev_consonant = False
            if prev_char_idx >= 0 and RE_KONSONAN.match(puisi[prev_char_idx]):
                has_prev_consonant = True
            
            # Cek apakah diikuti oleh satu konsonan diikuti vokal
            next_consonant_and_vowel = False
            next_idx = next((i for i, (pos, _, _) in enumerate(vokal_posisi) if pos > idx), None)
            if next_idx is not None:
                next_vowel_idx = vokal_posisi[next_idx][0]
                between_text = puisi[idx + 1:next_vowel_idx]
                if (' ' not in between_text and 
                    sum(1 for c in between_text if RE_KONSONAN.match(c)) == 1):
                    next_consonant_and_vowel = True
            
            valid_pattern = has_prev_consonant and next_consonant_and_vowel
            pattern_info = "✓" if valid_pattern else "✗"
            
            vokal_debug.append(f"{char}({met}){pattern_info}")
        
        hasil.append(f"Vokal dengan metrum dan pola: {' '.join(vokal_debug)}")
        hasil.append("✓ = vokal dalam pola yang valid untuk perubahan pendek/panjang")
        hasil.append("✗ = vokal dalam pola yang tidak valid untuk perubahan pendek/panjang")
        hasil.append("")
    
    return "\n".join(hasil)

'''    
'''
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
                            if len(konsonan_setelah_v1) == 1 and v1_lower in VOWEL_PENDEK:
                                hasil_line[idx2] = ZWNJ + v2.upper()
                                i_vokal += 2
                                continue
            # Logika pemanjangan vokal
            if (i_vokal + 2) < len(vokal_posisi):
                idx3, v3, met3 = vokal_posisi[i_vokal + 2]
                if v1_lower in 'aiu' and met1 == '–': # Vokal pendek a, i, u pada metrum panjang
                    prev_char_idx = idx1 - 1
                    next1_char_idx = idx1 + 1
                    next2_char_idx = idx1 + 2

                    if (prev_char_idx >= 0 and next2_char_idx < len(line)):
                        prev_char = line[prev_char_idx]
                        next1_char = line[next1_char_idx]
                        next2_char = line[next2_char_idx]
                        
                        if (RE_KONSONAN.match(prev_char) and RE_KONSONAN.match(next1_char) and RE_VOKAL.match(next2_char)):
                            if v1_lower == 'a':
                                hasil_line[idx1] = 'ā'
                            elif v1_lower == 'i':
                                hasil_line[idx1] = 'ī'
                            elif v1_lower == 'u':
                                hasil_line[idx1] = 'ū'
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
'''
