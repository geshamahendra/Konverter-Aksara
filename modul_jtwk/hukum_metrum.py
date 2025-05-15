import re

RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ]')
RE_KONSONAN = re.compile(r'[bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk]')
ZWNJ = '\u200C'
VOWELS = 'aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOWEL_PENDEK = 'aiuĕAIUĔ'
VOWEL_PANJANG = 'āâîīûūêôeèéoöꜽꜷĀÂÎĪÛŪÊÔÉÈÖŌꜼꜶ'
KHUSUS_KONSONAN = 'ṅŋḥṙ'
TANDA_SALAH = '❌'
JARAK_TANDA_SALAH = 3

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
            processed_vokal = False  # Flag untuk menandai apakah vokal sudah diproses


            

            # Logika untuk kasus "vokal spasi vokal"
            if re.fullmatch(r'[^\S\n]+', text_between):
                if met1 == '⏑' and met2 == '⏑':
                    if v1_lower in VOWEL_PENDEK and v2_lower in VOWEL_PENDEK:
                        hasil_line[idx2] = ZWNJ + v2.upper()
                        i_vokal += 2
                        processed_vokal = True
                elif v1_lower in VOWEL_PENDEK and v2_lower in VOWELS and met1 == '⏑' and met2 == '–':
                    hasil_line[idx2] = ZWNJ + v2.upper()
                    i_vokal += 2
                    processed_vokal = True
                elif v1_lower in VOWEL_PANJANG and v2_lower in VOWELS and met1 == '–' and met2 == '⏑':
                    hasil_line[idx2] = ZWNJ + v2.upper()
                    i_vokal += 2
                    processed_vokal = True

            # Logika untuk kasus "vokal konsonan spasi vokal"
            elif not processed_vokal and met1 == '–' and v1_lower in VOWEL_PENDEK and ' ' in text_between:
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
                                processed_vokal = True
            
            # =================================================================
            # Bagian Logika Pemanjangan dan Pemendekan Vokal
            # =================================================================
            if not processed_vokal and i_vokal < len(vokal_posisi):
                idx_vokal, vokal, metrum_vokal = vokal_posisi[i_vokal]
                vokal_lower = vokal.lower()
                # Logika Pemanjangan Vokal
                if vokal_lower in 'aiu' and metrum_vokal == '–':
                    next1_idx = idx_vokal + 1
                    next2_idx = idx_vokal + 2
                    if next2_idx < len(line):
                        char1 = line[next1_idx]
                        char2 = line[next2_idx]
                        if RE_KONSONAN.match(char1) and RE_VOKAL.match(char2):
                            if vokal_lower == 'a':
                                hasil_line[idx_vokal] = 'ā'  # Pemanjangan 'a' menjadi 'ā'
                            elif vokal_lower == 'i':
                                hasil_line[idx_vokal] = 'ī'  # Pemanjangan 'i' menjadi 'ī'
                            elif vokal_lower == 'u':
                                hasil_line[idx_vokal] = 'ū'  # Pemanjangan 'u' menjadi 'ū'

                # Logika Pemendekan Vokal
                elif vokal_lower in 'āīū' and metrum_vokal == '⏑':
                     if vokal_lower == 'ā':
                         hasil_line[idx_vokal] = 'a'
                     elif vokal_lower == 'ī':
                         hasil_line[idx_vokal] = 'i'
                     elif vokal_lower == 'ū':
                         hasil_line[idx_vokal] = 'u'
                i_vokal += 1
            elif processed_vokal:
                pass # Jika vokal sudah diproses, i_vokal sudah ditambah
            else:
                i_vokal += 1 # Jika tidak ada perubahan pada pasangan vokal ini

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
        header_blok = [b for b in baris if (b.startswith("<") and ":" in b) or
                                           (b.startswith("{") and ":" in b)]
        puisi_baris = [b for b in baris if not RE_METRUM_SIMBOL.search(b) and
                                           not (b.startswith("<") and ":" in b or
                                                b.startswith("{") and ":" in b)]
        metrum_baris_temp = [get_clean_metrum(b) for b in baris if RE_METRUM_SIMBOL.search(b)]

        hasil_blok.extend(header_blok)

        if is_metrum_blok:
            current_metrum = metrum_baris_temp
            hasil_blok.extend(baris) # Sertakan kembali baris metrum dalam output
        elif current_metrum: # Hanya proses jika ada metrum yang tersimpan (dari blok sebelumnya)
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

            # Cek kesesuaian dan tandai error
            processed_with_error = []
            for i, processed_line in enumerate(processed_puisi):
                jumlah_vokal = sum(1 for char in processed_line if char.lower() in VOWELS)
                jumlah_metrum_baris = len(current_metrum[i % len(current_metrum)]) if current_metrum else 0
                if jumlah_vokal != jumlah_metrum_baris and jumlah_metrum_baris != 0:
                    processed_with_error.append(processed_line + " " * JARAK_TANDA_SALAH + TANDA_SALAH)
                else:
                    processed_with_error.append(processed_line)
            hasil_blok.extend(processed_with_error)
        else:
            hasil_blok.extend(puisi_baris) # Jika ini blok bait pertama dan belum ada metrum

        hasil_blok.append("") # Tambahkan baris kosong antar blok

    return "\n".join(hasil_blok).strip()

def tandai_vokal_pendek_dalam_pasangan(text):
    """
    Fungsi ini memproses teks puisi untuk menandai vokal pendek yang berada dalam
    pasangan dengan vokal pendek lainnya dalam satu kata, sesuai dengan aturan metrum.
    Fungsi ini juga menghitung jumlah metrum pada baris metrum dan menandai
    ketidaksesuaian antara jumlah vokal dan simbol metrum.

    Args:
        text (str): Teks puisi yang akan diproses.

    Returns:
        str: Teks puisi yang sudah diproses, dengan vokal pendek yang ditandai,
             jumlah metrum pada baris metrum, dan penandaan ketidaksesuaian
             jumlah vokal dan simbol metrum.
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
            elif line.startswith("{") and ":" in line: # perubahan disini
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
            #cek kesesuaian disini
            for i, processed_line in enumerate(processed):
                jumlah_vokal = sum(1 for char in processed_line if char.lower() in VOWELS)
                if current_metrum and len(current_metrum) > 0:
                  jumlah_metrum_baris = len(current_metrum[i % len(current_metrum)])
                else:
                   jumlah_metrum_baris = 0
                if jumlah_vokal != jumlah_metrum_baris and jumlah_metrum_baris != 0:
                    processed[i] = processed_line + " " * JARAK_TANDA_SALAH + TANDA_SALAH
            hasil_blok.extend(processed)
        hasil_blok.append("")
    hasil_akhir = "\n".join(hasil_blok).strip()
    return hasil_akhir

#backup paling stabil, tanpa pengecekan x
'''
import re

RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéöoꜽꜷAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ]')
RE_KONSONAN = re.compile(r'[bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳk]')
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
            # =================================================================
            # Bagian Logika Pemanjangan dan Pemendekan Vokal
            # =================================================================
            if i_vokal < len(vokal_posisi):
                idx_vokal, vokal, metrum_vokal = vokal_posisi[i_vokal]
                vokal_lower = vokal.lower()

                # Logika Pemanjangan Vokal
                if vokal_lower in 'aiu' and metrum_vokal == '–':
                    next1_idx = idx_vokal + 1
                    next2_idx = idx_vokal + 2
                    if next2_idx < len(line):
                        char1 = line[next1_idx]
                        char2 = line[next2_idx]
                        if RE_KONSONAN.match(char1) and RE_VOKAL.match(char2):
                            if vokal_lower == 'a':
                                hasil_line[idx_vokal] = 'ā'  # Pemanjangan 'a' menjadi 'ā'
                            elif vokal_lower == 'i':
                                hasil_line[idx_vokal] = 'ī'  # Pemanjangan 'i' menjadi 'ī'
                            elif vokal_lower == 'u':
                                hasil_line[idx_vokal] = 'ū'  # Pemanjangan 'u' menjadi 'ū'

                # Logika Pemendekan Vokal
                elif vokal_lower in 'āīū' and metrum_vokal == '⏑':
                     if vokal_lower == 'ā':
                         hasil_line[idx_vokal] = 'a'
                     elif vokal_lower == 'ī':
                         hasil_line[idx_vokal] = 'i'
                     elif vokal_lower == 'ū':
                         hasil_line[idx_vokal] = 'u'
            # =================================================================
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
    ada_metrum = False # Flag untuk menandai apakah ada metrum di blok sebelumnya

    for blok in blok_list:
        baris = blok.strip().splitlines()
        # Modifikasi di sini untuk menyertakan { dan }
        is_metrum_blok = any(RE_METRUM_SIMBOL.search(b) for b in baris)
        header_blok = [b for b in baris if (b.startswith("<") and ":" in b) or 
                                           (b.startswith("{") and ":" in b)] # perubahan disini
        puisi_baris = [b for b in baris if not RE_METRUM_SIMBOL.search(b) and 
                                           not (b.startswith("<") and ":" in b or 
                                                b.startswith("{") and ":" in b)] # perubahan disini
        metrum_baris_temp = [get_clean_metrum(b) for b in baris if RE_METRUM_SIMBOL.search(b)]

        hasil_blok.extend(header_blok)

        if is_metrum_blok:
            current_metrum = metrum_baris_temp
            hasil_blok.extend(baris) # Sertakan kembali baris metrum dalam output
            ada_metrum = len(metrum_baris_temp) > 0 # Set flag jika ada baris metrum
        elif ada_metrum: # Hanya proses jika ada metrum di blok sebelumnya
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
            ada_metrum = False # Reset flag setelah pemrosesan
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
            elif line.startswith("{") and ":" in line: # perubahan disini
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