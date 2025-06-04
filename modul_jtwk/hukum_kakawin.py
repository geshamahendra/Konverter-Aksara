
import re

RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéōöŏoꜽꜷAĀÂIĪÎUŪÛOŎŌÔEÊÉÈꜼꜶ]')
RE_KONSONAN = re.compile(r'[bcdfghjɉklmnpꝑqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳŋḥṙ]')
ZWNJ = '\u200C'
ZWJ = '\u200D'
VOWELS = 'aiuĕāâîīûūêôeèéöoōŏꜽꜷAĀÂIĪÎUŪÛO‌ŎŌÔEÊÉÈꜼꜶ'
VOWEL_PENDEK = 'aiuĕAIUĔ'
VOWEL_PANJANG = 'āâîīûūêôeèéoōöŏꜽꜷĀÂÎĪÛŪÊŎÔÉÈÖŌꜼꜶ'
KHUSUS_KONSONAN = 'ṅŋḥṙ'
TANDA_SALAH = '❌'
JARAK_TANDA_SALAH = 2
konsonan_pattern = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṛṝḷḹꝁǥꞓƀśḳ"

# Kamus Pemetaan Vokal (Bisa didefinisikan secara global jika digunakan di banyak tempat)
VOWEL_PENDEK_KE_PANJANG = {
    'a': 'ā',
    'i': 'ī',
    'u': 'ū',
    'ĕ': 'ö',
}

VOWEL_PANJANG_KE_PENDEK = {
    'ā': 'a', 'â': 'a',
    'ī': 'i', 'î': 'i',
    'ū': 'u', 'û': 'u',
    'ö': 'ĕ', 'e': 'ĕ', 'è': 'ĕ', 'é': 'ĕ',
}

def bersihkan_karakter_tak_terlihat(text):
    """
    Membersihkan karakter tak terlihat (zero-width non-joiner, spasi) dari text.

    Args:
        text (str): Teks yang akan dibersihkan.

    Returns:
        str: Teks yang sudah dibersihkan.
    """
    return re.sub(r'[\u200C\u200D\s-]', '', text)

def get_clean_metrum(line):
    """
    Mengekstrak simbol-simbol metrum dari sebuah baris text.  Menangani pengulangan metrum.

    Args:
        line (str): Baris text yang mengandung simbol metrum.

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
    Menghitung jumlah simbol metrum dalam sebuah baris text, termasuk yang ada dalam pengulangan.

    Args:
        line (str): Baris text yang mengandung simbol metrum.

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

# --- Fungsi Pembantu ---
def ubah_vokal_sesuai_metrum(vokal_char, metrum_target, is_first_char=False):
    """
    Mengubah vokal berdasarkan metrum target.
    Args:
        vokal_char (str): Karakter vokal asli.
        metrum_target (str): Simbol metrum yang dituju ('–' untuk panjang, '⏑' untuk pendek).
        is_first_char (bool): True jika vokal adalah karakter pertama baris (untuk kapitalisasi).

    Returns:
        str: Vokal yang sudah diubah atau vokal asli jika tidak ada perubahan.
    """
    vokal_lower = vokal_char.lower()
    
    if metrum_target == '–': # Metrum panjang, coba panjangkan
        if vokal_lower in VOWEL_PENDEK_KE_PANJANG:
            transformed_vowel = VOWEL_PENDEK_KE_PANJANG[vokal_lower]
            return transformed_vowel.upper() if is_first_char else transformed_vowel
    elif metrum_target == '⏑': # Metrum pendek, coba pendekkan
        if vokal_lower in VOWEL_PANJANG_KE_PENDEK:
            transformed_vowel = VOWEL_PANJANG_KE_PENDEK[vokal_lower]
            return transformed_vowel.upper() if is_first_char else transformed_vowel
    
    # Jika tidak ada perubahan atau vokal tidak ada dalam kamus pemetaan
    # Pertahankan kapitalisasi asli jika bukan karakter pertama, atau kapitalisasi pertama jika diminta
    if is_first_char:
        return vokal_char.upper()
    return vokal_char


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
        
        # Bersihkan karakter tak terlihat untuk matching vokal dengan metrum
        clean_line = bersihkan_karakter_tak_terlihat(line)
        
        # PERBAIKAN: Periksa vokal di awal baris dengan pola VCV
        if clean_line and RE_VOKAL.match(clean_line[0]):
            metrum_awal = selected_metrum[0]  # Metrum untuk posisi pertama
            vokal_awal = clean_line[0] # Ambil karakter asli untuk diubah

            # Periksa apakah vokal diikuti oleh pola konsonan-vokal (CV)
            if len(clean_line) >= 3:
                if (RE_KONSONAN.match(clean_line[1]) and 
                    RE_VOKAL.match(clean_line[2]) and 
                    clean_line[1].lower() not in KHUSUS_KONSONAN):
                    
                    # Gunakan fungsi pembantu untuk pemanjangan/pemendekan
                    new_vokal_awal = ubah_vokal_sesuai_metrum(vokal_awal, metrum_awal, is_first_char=True)
                    if new_vokal_awal != vokal_awal:
                        line = new_vokal_awal + line[1:]
        
        # Temukan semua posisi vokal dalam baris bersih untuk dikaitkan dengan metrum
        vokal_posisi_clean = []
        for idx, char in enumerate(clean_line):
            if char.lower() in VOWELS:
                vokal_posisi_clean.append(idx)
        
        # Pemetaan indeks vokal baris bersih ke baris asli
        vokal_posisi = []
        clean_idx = 0  # Indeks saat ini di clean_line
        orig_idx = 0   # Indeks saat ini di line asli
        clean_vokal_idx = 0  # Indeks saat ini di vokal_posisi_clean
        
        while clean_idx < len(clean_line) and clean_vokal_idx < len(vokal_posisi_clean):
            if clean_idx == vokal_posisi_clean[clean_vokal_idx]:
                while orig_idx < len(line):
                    if line[orig_idx].lower() in VOWELS:
                        metrum_idx = clean_vokal_idx % len(selected_metrum)
                        vokal_posisi.append((orig_idx, line[orig_idx], selected_metrum[metrum_idx]))
                        orig_idx += 1
                        break
                    orig_idx += 1
                clean_vokal_idx += 1
            clean_idx += 1
            
            while orig_idx < len(line) and (line[orig_idx] == ZWNJ or line[orig_idx] == ZWJ):
                orig_idx += 1

        hasil_line = list(line)
        
        kata_kata = list(re.finditer(r'\S+', line))
        kata_list = [(m.start(), m.end(), m.group()) for m in kata_kata]

        i_vokal = 0
        while i_vokal < len(vokal_posisi) - 1:
            idx1, v1, met1 = vokal_posisi[i_vokal]
            idx2, v2, met2 = vokal_posisi[i_vokal + 1]
            v1_lower, v2_lower = v1.lower(), v2.lower()
            text_between = line[idx1 + 1:idx2]

            # Logika untuk kasus "vokal spasi vokal"
            if re.fullmatch(r'[^\S\n]*', text_between):
                # Ini lebih tentang kapitalisasi, bukan pemanjangan/pemendekan struktural
                # Jadi logika aslinya mungkin tetap relevan di sini jika memang hanya kapitalisasi yang diinginkan
                if met1 == '⏑' and met2 == '⏑' and v1_lower in VOWEL_PENDEK and v2_lower in VOWEL_PENDEK:
                    hasil_line[idx2] = v2.upper()
                    i_vokal += 1
                    continue
                elif v1_lower in VOWEL_PENDEK and v2_lower in VOWELS and met1 == '⏑' and met2 == '–':
                    hasil_line[idx2] = v2.upper()
                    i_vokal += 1
                    continue
                elif v1_lower in VOWEL_PANJANG and v2_lower in VOWELS and met1 == '–' and met2 == '⏑':
                    hasil_line[idx2] = v2.upper()
                    i_vokal += 1
                    continue
                elif v1_lower in VOWEL_PANJANG and v2_lower in VOWELS and met1 == '–' and met2 == '–':
                    hasil_line[idx2] = v2.upper()
                    i_vokal += 1
                    continue

            # Logika untuk kasus "vokal konsonan spasi vokal"
            if met1 == '–' and v1_lower in VOWEL_PENDEK:
                kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                if kata_v1 and kata_v2 and kata_v1 != kata_v2:
                    akhir_kata1 = kata_v1[2]
                    awal_kata2 = kata_v2[2]
                    idx_v1_relatif = idx1 - kata_v1[0]
                    if idx_v1_relatif + 1 < len(akhir_kata1):
                        konsonan_akhir_kata1 = akhir_kata1[idx_v1_relatif + 1]
                        if RE_KONSONAN.match(konsonan_akhir_kata1) and awal_kata2 and awal_kata2[0].lower() == v2_lower and ' ' in text_between:
                            # Ini juga lebih ke kapitalisasi
                            hasil_line[idx2] = v2.upper()
                            i_vokal += 1
                            continue

            # Kasus "vokal saat ini + spasi + satu konsonan + vokal lain" (seperti "wāna ra")
            # Pemanjangan
            if met1 == '–' and v1_lower in VOWEL_PENDEK:
                konsonan_pattern = RE_KONSONAN.pattern[1:-1]
                vokal_spasi_konsonan_pattern = re.fullmatch(r'\s+([' + konsonan_pattern + '])\s*', text_between)
                if vokal_spasi_konsonan_pattern and vokal_spasi_konsonan_pattern.group(1).lower() not in KHUSUS_KONSONAN:
                    konsonan = vokal_spasi_konsonan_pattern.group(1)
                    kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                    if kata_v2:
                        awal_kata2 = kata_v2[2]
                        if awal_kata2.startswith(konsonan) and len(awal_kata2) > 1 and RE_VOKAL.match(awal_kata2[1]):
                            new_vokal = ubah_vokal_sesuai_metrum(v1, met1)
                            if new_vokal != v1:
                                hasil_line[idx1] = new_vokal
            # Pemendekan
            elif met1 == '⏑' and v1_lower in VOWEL_PANJANG:
                konsonan_pattern = RE_KONSONAN.pattern[1:-1]
                vokal_spasi_konsonan_pattern = re.fullmatch(r'\s+([' + konsonan_pattern + '])\s*', text_between)
                if vokal_spasi_konsonan_pattern and vokal_spasi_konsonan_pattern.group(1).lower() not in KHUSUS_KONSONAN:
                    konsonan = vokal_spasi_konsonan_pattern.group(1)
                    kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                    if kata_v2:
                        awal_kata2 = kata_v2[2]
                        if awal_kata2.startswith(konsonan) and len(awal_kata2) > 1 and RE_VOKAL.match(awal_kata2[1]):
                            new_vokal = ubah_vokal_sesuai_metrum(v1, met1)
                            if new_vokal != v1:
                                hasil_line[idx1] = new_vokal

            # Khusus untuk pola seperti "wāna ra" (akhir kata vokal + awal kata konsonan+vokal)
            # Pemanjangan
            if met1 == '–' and v1_lower in VOWEL_PENDEK:
                kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                if kata_v1:
                    kata = kata_v1[2]
                    idx_rel = idx1 - kata_v1[0]
                    if idx_rel == len(kata) - 1: # Vokal di akhir kata
                        next_kata_idx = kata_list.index(kata_v1) + 1
                        if next_kata_idx < len(kata_list):
                            next_kata = kata_list[next_kata_idx][2]
                            if len(next_kata) == 2 and RE_KONSONAN.match(next_kata[0]) and RE_VOKAL.match(next_kata[1]):
                                if next_kata[0].lower() not in KHUSUS_KONSONAN:
                                    new_vokal = ubah_vokal_sesuai_metrum(v1, met1)
                                    if new_vokal != v1:
                                        hasil_line[idx1] = new_vokal
            # Pemendekan
            elif met1 == '⏑' and v1_lower in VOWEL_PANJANG:
                kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                if kata_v1:
                    kata = kata_v1[2]
                    idx_rel = idx1 - kata_v1[0]
                    if idx_rel == len(kata) - 1:
                        next_kata_idx = kata_list.index(kata_v1) + 1
                        if next_kata_idx < len(kata_list):
                            next_kata = kata_list[next_kata_idx][2]
                            if len(next_kata) == 2 and RE_KONSONAN.match(next_kata[0]) and RE_VOKAL.match(next_kata[1]):
                                if next_kata[0].lower() not in KHUSUS_KONSONAN:
                                    new_vokal = ubah_vokal_sesuai_metrum(v1, met1)
                                    if new_vokal != v1:
                                        hasil_line[idx1] = new_vokal

            # Kasus KVKV dalam kata yang sama
            # Ini adalah loop utama untuk setiap vokal, jadi saya biarkan logika di sini.
            # Dapatkan semua konsonan dengan mengecualikan karakter khusus
            konsonan_pattern = RE_KONSONAN.pattern[1:-1]
            vokal_konsonan_pattern = re.search(r'^(\s+)([' + konsonan_pattern + '])(' + RE_VOKAL.pattern[1:-1] + ')', text_between, re.IGNORECASE)
            
            if vokal_konsonan_pattern:
                konsonan = vokal_konsonan_pattern.group(2)
                if konsonan.lower() not in KHUSUS_KONSONAN:
                    new_vokal = ubah_vokal_sesuai_metrum(v1, met1)
                    if new_vokal != v1:
                        hasil_line[idx1] = new_vokal

            i_vokal += 1
        
        # MODIFIKASI: Sekarang pemanjangan dan pemendekan vokal memeriksa pola KVKV dalam kata yang sama
        for i, (idx_vokal, vokal, metrum_vokal) in enumerate(vokal_posisi):
            vokal_lower = vokal.lower()
            
            kata_v = next((k for k in kata_list if k[0] <= idx_vokal < k[1]), None)
            
            if kata_v:
                kata = kata_v[2]
                idx_rel = idx_vokal - kata_v[0]
                
                # Cek apakah vokal ini didahului oleh konsonan (pola KVKV)
                konsonan_sebelum = idx_rel > 0 and RE_KONSONAN.match(kata[idx_rel - 1])
                
                # Pemeriksaan pola KVKV dalam kata yang sama
                if (konsonan_sebelum and 
                    idx_rel + 2 < len(kata) and 
                    RE_KONSONAN.match(kata[idx_rel + 1]) and 
                    RE_VOKAL.match(kata[idx_rel + 2])):
                    
                    new_vokal = ubah_vokal_sesuai_metrum(vokal, metrum_vokal)
                    if new_vokal != vokal:
                        hasil_line[idx_vokal] = new_vokal

                # Logika untuk pola 2+ konsonan + vokal + 1 konsonan + 1 vokal
                konsonan_sebelum_count = 0
                temp_idx = idx_rel - 1
                while temp_idx >= 0 and RE_KONSONAN.match(kata[temp_idx]):
                    konsonan_sebelum_count += 1
                    temp_idx -= 1
                
                if (konsonan_sebelum_count >= 2 and 
                    idx_rel + 2 < len(kata) and 
                    RE_KONSONAN.match(kata[idx_rel + 1]) and 
                    RE_VOKAL.match(kata[idx_rel + 2])):
                    
                    konsonan_setelah = kata[idx_rel + 1]
                    if konsonan_setelah.lower() not in KHUSUS_KONSONAN:
                        new_vokal = ubah_vokal_sesuai_metrum(vokal, metrum_vokal)
                        if new_vokal != vokal:
                            hasil_line[idx_vokal] = new_vokal
                
        processed.append(''.join(hasil_line))
    return processed
    
def aplikasikan_metrum_dan_tandai_vokal(text):
    """
    Fungsi utama untuk mengaplikasikan metrum dan menandai vokal pada text puisi.
    Fungsi ini memproses text per blok, mengenali blok metrum dan blok bait,
    serta menerapkan aturan metrum yang sesuai.

    Args:
        text (str): Teks puisi yang akan diproses. Teks diharapkan memiliki format
                    blok metrum dan blok bait yang dipisahkan oleh baris kosong.

    Returns:
        str: Teks puisi yang sudah diproses, dengan penerapan metrum dan penandaan vokal.
    """
    blok_list = re.split(r'\n\s*\n', text.strip(), flags=re.MULTILINE)
    hasil_blok = []
    current_metrum = []

    for blok in blok_list:
        baris = blok.strip().splitlines()
        is_metrum_blok = any(RE_METRUM_SIMBOL.search(b) for b in baris)
        header_blok = [b for b in baris if (b.startswith("<") and ">" in b) or
                                           (b.startswith("{") and "}" in b) or
                                           (b.startswith("]") and "]" in b)or
                                           (b.startswith("[") and "[" in b)]
        puisi_baris = [b for b in baris if not RE_METRUM_SIMBOL.search(b) and
                                           not (b.startswith("<") and ">" in b or
                                                b.startswith("{") and "}" in b or
                                                b.startswith("]") and "]" in b or
                                                b.startswith("[") and "[" in b)]
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
                # Membersihkan karakter tak terlihat hanya untuk perhitungan jumlah vokal
                cleaned_line = bersihkan_karakter_tak_terlihat(processed_line)
                jumlah_vokal = sum(1 for char in cleaned_line if char.lower() in VOWELS)
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

def cek_kakawin(text):
    """
    Fungsi ini memproses text puisi untuk menandai vokal pendek yang berada dalam
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
            if line.startswith("<") and ">" in line:
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
            elif line.startswith("{") and "}" in line: # perubahan disini
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
            elif line.startswith("]") and "]" in line: # perubahan disini
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
            elif line.startswith("[") and "[" in line: # perubahan disini
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
                metrum_line = f"{line} = {jumlah}"
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
                # Membersihkan karakter tak terlihat hanya untuk perhitungan jumlah vokal
                cleaned_line = bersihkan_karakter_tak_terlihat(processed_line)
                jumlah_vokal = sum(1 for char in cleaned_line if char.lower() in VOWELS)
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