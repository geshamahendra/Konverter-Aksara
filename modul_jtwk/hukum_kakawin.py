import re

# --- Konfigurasi Global ---
TANDA_SALAH = '❌'
JARAK_TANDA_SALAH = 2

# Mengubah ENABLE_KONSONAN_GANDA_CHECK agar bisa diatur dengan 'true'/'false' (case-insensitive) atau '0'/'1'
# Anda bisa mengubah string di bawah ini menjadi 'true', 'false', '1', atau '0'
_ENABLE_KONSONAN_GANDA_CHECK_STR = '1' # <-- Ubah ini sesuai kebutuhan Anda

# Konversi string ke Boolean Python yang sebenarnya
# Jika nilai string adalah 'true' (case-insensitive) atau '1', maka akan jadi True.
# Selain itu, akan jadi False.
ENABLE_KONSONAN_GANDA_CHECK = _ENABLE_KONSONAN_GANDA_CHECK_STR.lower() in ('true', '1')

# --- Regex dan Konstanta Lainnya ---
RE_METRUM_SIMBOL = re.compile(r'[–⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéōöŏoꜽꜷAĀÂIĪÎUŪÛOŎŌÔEÊÉÈꜼꜶṝḹṛḷ❓]')
RE_KONSONAN = re.compile(r'[bcdfghjɉklmnpꝑqrstvwyzḋḍđŧṭṣñṇṅꝁǥꞓƀśḳŋḥṙʰ-]')
ZWNJ = '\u200C'
ZWJ = '\u200D'
# Definisi ṝḹṛḷ sebagai vokal
VOWELS = 'aiuĕāâîīûūêôeèéöoōŏꜽꜷĀÂÎĪÛŪÊŎÔŌꜼꜶṝḹṛḷ❓'
VOWEL_PENDEK = 'aiuĕAIUĔṛḷ❓'
VOWEL_PANJANG = 'āâîīûūêôeèéöoōŏꜽꜷĀÂÎĪÛŪÊŎÔŌṝḹ'
KHUSUS_KONSONAN = 'ṅŋḥṙ'
konsonan_pattern = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅꝁǥꞓƀśḳ"

# Kamus Pemetaan Vokal
VOWEL_PENDEK_KE_PANJANG = {
    'a': 'ā',
    'i': 'ī',
    'u': 'ū',
    'ĕ': 'ö',
    'ṛ': 'ṝ',
    'ḷ': 'ḹ',
    # 'ṛ': 'ṝ', # Duplikat, dihapus
    # 'ḷ': 'ḹ', # Duplikat, dihapus
}

VOWEL_PANJANG_KE_PENDEK = {
    'ā': 'a', 'â': 'a',
    'ī': 'i', 'î': 'i',
    'ū': 'u', 'û': 'u',
    'ö': 'ĕ', 'e': 'ĕ', 'è': 'ĕ', 'é': 'ĕ',
    'ō': 'o',
    'ṝ': 'ṛ',
    'ḹ': 'ḷ',
    'o': '❓', 'ꜷ': '❓', 'ꜽ': '❓',
}

# --- Kamus Pemetaanuntuk Normalisasi ---
# Ini akan mengubah karakter kapital khusus ke bentuk lowercase-nya atau padanannya
INIT_NORMALIZATION_MAP = {
    'rĕ': 'ṛ',
    'rö': 'ṝ',
    'lĕ': 'ḷ',
    'lö': 'ḹ',
    'Rĕ': 'ṛ',
    'Rö': 'ṝ',
    'Lĕ': 'ḷ',
    'Lö': 'ḹ',
}
FINAL_NORMALIZATION_MAP = {
    'Ṛ' : 'rĕ', # Mengubah kapital Ṛ (dari input atau kapitalisasi lain) ke ṛ
    'Ḷ': 'lĕ',  # Mengubah kapital Ḷ (dari input atau kapitalisasi lain) ke ḷ
    'Ṝ': 'rö',  # Mengubah kapital Ṝ ke ṛ
    'Ḹ': 'lö',  # Mengubah kapital Ḹ ke ḷ
    'ṛ': 'rĕ',
    'ṝ': 'rö',
    'ḷ': 'lĕ',
    'ḹ': 'lö',
}

def bersihkan_karakter_tak_terlihat(text):
    """
    Membersihkan karakter tak terlihat (zero-width non-joiner, spasi) dari text.
    """
    return re.sub(r'[\u200C\u200D\s-]', '', text)

def get_clean_metrum(line):
    """
    Mengekstrak simbol-simbol metrum dari sebuah baris text. Menangani pengulangan metrum.
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
    Akan mengkapitalisasi jika is_first_char dan kondisi lain terpenuhi.
    Normalisasi ke lowercase ṛ dan ḷ dilakukan di langkah akhir.
    """
    vokal_lower = vokal_char.lower()

    if metrum_target == '–': # Metrum panjang, coba panjangkan
        if vokal_lower in VOWEL_PENDEK_KE_PANJANG:
            transformed_vowel = VOWEL_PENDEK_KE_PANJANG[vokal_lower]
            # Kapitalisasi jika ini adalah karakter pertama baris
            return transformed_vowel.upper() if is_first_char else transformed_vowel
    elif metrum_target == '⏑': # Metrum pendek, coba pendekkan
        if vokal_lower in VOWEL_PANJANG_KE_PENDEK:
            transformed_vowel = VOWEL_PANJANG_KE_PENDEK[vokal_lower]
            # Kapitalisasi jika ini adalah karakter pertama baris
            return transformed_vowel.upper() if is_first_char else transformed_vowel
    
    # Jika tidak ada perubahan yang terjadi, tetap perhatikan kapitalisasi awal
    if is_first_char:
        return vokal_char.upper()
    return vokal_char


def proses_puisi_buffer(puisi_buffer, current_metrum):
    """
    Menerapkan metrum pada baris-baris puisi dalam buffer.
    Pengecekan konsonan ganda di antara vokal (mis. "anakku" -> "akku") dilakukan terakhir.
    """
    if not current_metrum:
        return puisi_buffer
    processed = []
    panjang_metrum = len(current_metrum)

    for i, line in enumerate(puisi_buffer):
        current_line_has_error_marker = False
        current_line_error_message = ""

        # --- Langkah Pra-pemrosesan Karakter Khusus (BARU) ---
        # Lakukan pemetaan dari kombinasi konsonan+vokal ke karakter khusus
        original_line = line # Simpan baris asli untuk referensi
        for old_seq, new_char in INIT_NORMALIZATION_MAP.items():
            # Menggunakan re.sub dengan fungsi pengganti untuk mempertahankan kapitalisasi awal jika diperlukan
            # Ini sedikit lebih kompleks karena PRA_PROSES_KARAKTER_KHUSUS memetakan 2 karakter menjadi 1
            # Kita perlu memastikan bahwa karakter khusus yang baru dimasukkan juga dihitung sebagai vokal
            # Cara paling sederhana adalah mengganti langsung dan memastikan regex VOWELS mengenalnya.
            # Ini juga berarti kita harus menangani UPPERCASE/lowercase di PRA_PROSES_KARAKTER_KHUSUS jika ada varian
            # Saat ini, saya mengasumsikan input 'rĕ' dll. adalah lowercase
            line = line.replace(old_seq, new_char)
            # Juga tangani kapitalisasi jika 'Rĕ' -> 'Ṛ', dll.
            line = line.replace(old_seq.capitalize(), new_char.upper())

        selected_metrum = current_metrum[i % panjang_metrum]

        clean_line_for_vowels = bersihkan_karakter_tak_terlihat(line)

        # Logika kapitalisasi huruf pertama baris
        if clean_line_for_vowels and RE_VOKAL.match(clean_line_for_vowels[0]):
            metrum_awal = selected_metrum[0]
            vokal_awal = clean_line_for_vowels[0]

            if len(clean_line_for_vowels) >= 3:
                # Periksa apakah ada konsonan + vokal setelah vokal awal
                if (RE_KONSONAN.match(clean_line_for_vowels[1]) and
                    RE_VOKAL.match(clean_line_for_vowels[2]) and
                    clean_line_for_vowels[1].lower() not in KHUSUS_KONSONAN):

                    # Panggil ubah_vokal_sesuai_metrum dengan is_first_char=True
                    # Ini akan mengkapitalisasi vokal awal jika perlu (termasuk ṛ/ḷ ke Ṛ/Ḷ atau ṝ/ḹ ke Ṝ/Ḹ)
                    new_vokal_awal = ubah_vokal_sesuai_metrum(vokal_awal, metrum_awal, is_first_char=True)
                    if new_vokal_awal != vokal_awal:
                        # Ganti hanya karakter vokal awal yang berubah di baris asli
                        # Temukan indeks karakter vokal awal di 'line'
                        idx_first_vowel_in_line = -1
                        temp_clean_idx_count = 0
                        for char_idx, char in enumerate(line):
                            if char.lower() in VOWELS:
                                if temp_clean_idx_count == 0:
                                    idx_first_vowel_in_line = char_idx
                                    break
                                temp_clean_idx_count += 1
                            elif char not in (ZWNJ, ZWJ, ' ', '-'): # Hanya karakter yang dihitung bersihkan_karakter_tak_terlihat
                                temp_clean_idx_count += 1
                        
                        if idx_first_vowel_in_line != -1:
                            hasil_line_temp = list(line)
                            hasil_line_temp[idx_first_vowel_in_line] = new_vokal_awal
                            line = "".join(hasil_line_temp)
                        # else: Ini berarti baris tidak memiliki vokal atau vokal awal tidak ditemukan, 
                        # yang seharusnya sudah ditangani oleh if clean_line_for_vowels dan RE_VOKAL.match

        vokal_posisi_clean = []
        for idx, char in enumerate(bersihkan_karakter_tak_terlihat(line)): # Gunakan 'line' yang sudah diubah
            if char.lower() in VOWELS:
                vokal_posisi_clean.append(idx)

        vokal_posisi_in_original_line = []
        clean_idx = 0
        orig_idx = 0
        clean_vokal_idx = 0

        while clean_idx < len(bersihkan_karakter_tak_terlihat(line)) and clean_vokal_idx < len(vokal_posisi_clean):
            if clean_idx == vokal_posisi_clean[clean_vokal_idx]:
                while orig_idx < len(line):
                    if line[orig_idx].lower() in VOWELS:
                        metrum_idx = clean_vokal_idx % len(selected_metrum)
                        vokal_posisi_in_original_line.append((orig_idx, line[orig_idx], selected_metrum[metrum_idx]))
                        orig_idx += 1
                        break
                    orig_idx += 1
                clean_vokal_idx += 1
            clean_idx += 1

            while orig_idx < len(line) and (line[orig_idx] == ZWNJ or line[orig_idx] == ZWJ):
                orig_idx += 1

        hasil_line = list(line) # Inisialisasi hasil_line dengan 'line' yang mungkin sudah berubah

        kata_kata = list(re.finditer(r'\S+', line))
        kata_list = [(m.start(), m.end(), m.group()) for m in kata_kata]

        # --- LOGIKA PENGUBAHAN VOKAL DAN KONSONAN YANG SUDAH ADA ---
        for i_vokal_curr, (idx_vokal, vokal, metrum_vokal) in enumerate(vokal_posisi_in_original_line):
            vokal_lower = vokal.lower()

            idx1, v1, met1 = vokal_posisi_in_original_line[i_vokal_curr]
            if i_vokal_curr + 1 < len(vokal_posisi_in_original_line):
                idx2, v2, met2 = vokal_posisi_in_original_line[i_vokal_curr + 1]
                v1_lower_temp, v2_lower_temp = v1.lower(), v2.lower()
                text_between = line[idx1 + 1:idx2]

                # --- PENAMBAHAN LOGIKA VOKAL BERURUTAN (misal: aaiiuu) ---
                # Pengecekan jika tidak ada konsonan di antara dua vokal DAN tidak ada spasi
                if ' ' not in text_between and not re.search(RE_KONSONAN, text_between):
                    # Jika metrum saat ini panjang dan vokal saat ini pendek
                    if met1 == '–' and v1_lower_temp in VOWEL_PENDEK:
                        new_vokal = ubah_vokal_sesuai_metrum(v1, met1) # is_first_char=False di sini
                        if new_vokal != v1:
                            hasil_line[idx1] = new_vokal
                    # Jika metrum saat ini pendek dan vokal saat ini panjang
                    elif met1 == '⏑' and v1_lower_temp in VOWEL_PANJANG:
                        new_vokal = ubah_vokal_sesuai_metrum(v1, met1) # is_first_char=False di sini
                        if new_vokal != v1:
                            hasil_line[idx1] = new_vokal

                if re.fullmatch(r'[^\S\n]*', text_between):
                    if met1 == '⏑' and met2 == '⏑' and v1_lower_temp in VOWELS and v2_lower_temp in VOWELS: #v2_lower_temp in VOWEL_PENDEK
                        hasil_line[idx2] = v2.upper()
                    elif v1_lower_temp in VOWELS and v2_lower_temp in VOWELS and met1 == '⏑' and met2 == '–': #VOWEL_PENDEK
                        hasil_line[idx2] = v2.upper()
                    elif v1_lower_temp in VOWELS and v2_lower_temp in VOWELS and met1 == '–' and met2 == '⏑': #VOWEL_PANJANG
                        hasil_line[idx2] = v2.upper()
                    elif v1_lower_temp in VOWELS and v2_lower_temp in VOWELS and met1 == '–' and met2 == '–': #VOWEL_PANJANG
                        hasil_line[idx2] = v2.upper()

                # vokal+konsonan+spasi+vokal
                if met1 == '–' and v1_lower_temp in VOWEL_PENDEK:
                    kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                    kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                    if kata_v1 and kata_v2 and kata_v1 != kata_v2:
                        akhir_kata1 = kata_v1[2]
                        idx_v1_relatif = idx1 - kata_v1[0]
                        if idx_v1_relatif + 1 < len(akhir_kata1):
                            konsonan_akhir_kata1 = akhir_kata1[idx_v1_relatif + 1]
                            if RE_KONSONAN.match(konsonan_akhir_kata1) and (konsonan_akhir_kata1.lower()) and ' ' in text_between:
                                if kata_v2 and len(kata_v2[2]) > 0 and kata_v2[2][0].lower() == v2_lower_temp:
                                    hasil_line[idx2] = v2.upper()
                
                # --- BLOK LOGIKA BARU UNTUK SKENARIO ANDA ---
                # Kondisi: vokal1 pendek, metrum vokal1 pendek, vokal2 di awal kata, metrum vokal2 panjang
                if met1 == '⏑' and v1_lower_temp in VOWEL_PENDEK: # Vokal 1 pendek dan metrumnya pendek
                    # Pastikan ada vokal kedua yang valid
                    if i_vokal_curr + 1 < len(vokal_posisi_in_original_line):
                        idx2, v2, met2 = vokal_posisi_in_original_line[i_vokal_curr + 1] # Ambil detail vokal 2

                        kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                        kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                        
                        # Pastikan vokal 1 dan 2 berbeda kata, ada konsonan di antara vokal 1 & spasi
                        if kata_v1 and kata_v2 and kata_v1 != kata_v2:
                            akhir_kata1 = kata_v1[2]
                            idx_v1_relatif = idx1 - kata_v1[0]
                            if idx_v1_relatif + 1 < len(akhir_kata1):
                                konsonan_akhir_kata1 = akhir_kata1[idx_v1_relatif + 1]
                                
                                # Cek konsonan setelah vokal pertama, spasi, dan vokal kedua di awal kata
                                if RE_KONSONAN.match(konsonan_akhir_kata1) and (konsonan_akhir_kata1.lower() not in KHUSUS_KONSONAN) and ' ' in line[idx1+1:idx2]:
                                    if kata_v2 and len(kata_v2[2]) > 0 and kata_v2[2][0].lower() == v2.lower(): # Pastikan v2 adalah awal kata kedua
                                        
                                        # --- TAMBAHAN LOGIKA BARU DI SINI ---
                                        # Cek apakah setelah vokal kedua hanya ada satu konsonan saja (misal: "atisaya", bukan "anntila")
                                        # Kita perlu memeriksa karakter kedua dari kata_v2 (yaitu kata_v2[2][1])
                                        # dan memastikan karakter ketiga bukan konsonan.
                                        
                                        is_single_consonant_after_v2 = False
                                        if len(kata_v2[2]) >= 2 and RE_KONSONAN.match(kata_v2[2][1]) and kata_v2[2][1].lower() not in KHUSUS_KONSONAN:
                                            # Jika ada karakter kedua dan itu konsonan (dan bukan konsonan khusus)
                                            if len(kata_v2[2]) == 2: # Kata hanya punya vokal dan satu konsonan
                                                is_single_consonant_after_v2 = True
                                            elif len(kata_v2[2]) > 2:
                                                # Pastikan karakter ketiga BUKAN konsonan
                                                if not RE_KONSONAN.match(kata_v2[2][2]) or kata_v2[2][2].lower() in KHUSUS_KONSONAN:
                                                    is_single_consonant_after_v2 = True
                                            
                                        # Hanya lanjutkan jika ada satu konsonan setelah vokal kedua ATAU jika vokal kedua adalah karakter terakhir kata
                                        if is_single_consonant_after_v2 or len(kata_v2[2]) == 1: # Tambahan: atau jika kata hanya terdiri dari vokal itu sendiri
                                            # Kondisi terakhir: metrum vokal 2 harus panjang
                                            if met2 == '–': # Metrum vokal kedua adalah panjang
                                                # Lakukan pemanjangan vokal kedua
                                                new_vokal_v2 = ubah_vokal_sesuai_metrum(v2, met2) # met2 harusnya '–' di sini
                                                if new_vokal_v2 != v2:
                                                    hasil_line[idx2] = new_vokal_v2
                                            # Tambahkan juga jika metrum vokal 2 pendek dan vokal 2 awalnya panjang,
                                            # maka pendekkan vokal kedua. (Jika ini yang Anda inginkan juga)
                                            elif met2 == '⏑' and v2.lower() in VOWEL_PANJANG:
                                                new_vokal_v2 = ubah_vokal_sesuai_metrum(v2, met2) # met2 harusnya '⏑' di sini
                                                if new_vokal_v2 != v2:
                                                    hasil_line[idx2] = new_vokal_v2

                if met1 == '–' and v1_lower_temp in VOWEL_PENDEK:
                    konsonan_pattern_str = RE_KONSONAN.pattern[1:-1]
                    vokal_spasi_konsonan_pattern = re.fullmatch(r'\s+' + r'([' + konsonan_pattern_str + r'])\s*', text_between)
                    if vokal_spasi_konsonan_pattern and vokal_spasi_konsonan_pattern.group(1).lower() not in KHUSUS_KONSONAN:
                        konsonan = vokal_spasi_konsonan_pattern.group(1)
                        kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                        if kata_v2:
                            awal_kata2 = kata_v2[2]
                            if awal_kata2.startswith(konsonan) and len(awal_kata2) > 1 and RE_VOKAL.match(awal_kata2[1]):
                                new_vokal = ubah_vokal_sesuai_metrum(v1, met1) 
                                if new_vokal != v1:
                                    hasil_line[idx1] = new_vokal

                elif met1 == '⏑' and v1_lower_temp in VOWEL_PANJANG:
                    konsonan_pattern_str = RE_KONSONAN.pattern[1:-1]
                    vokal_spasi_konsonan_pattern = re.fullmatch(r'\s+' + r'([' + konsonan_pattern_str + r'])\s*', text_between)
                    if vokal_spasi_konsonan_pattern and vokal_spasi_konsonan_pattern.group(1).lower() not in KHUSUS_KONSONAN:
                        konsonan = vokal_spasi_konsonan_pattern.group(1)
                        kata_v2 = next((k for k in kata_list if k[0] <= idx2 < k[1]), None)
                        if kata_v2:
                            awal_kata2 = kata_v2[2]
                            if awal_kata2.startswith(konsonan) and len(awal_kata2) > 1 and RE_VOKAL.match(awal_kata2[1]):
                                new_vokal = ubah_vokal_sesuai_metrum(v1, met1) 
                                if new_vokal != v1:
                                    hasil_line[idx1] = new_vokal

                if met1 == '–' and v1_lower_temp in VOWEL_PENDEK:
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
                                        new_vokal = ubah_vokal_sesuai_metrum(v1, met1) # is_first_char=False di sini
                                        if new_vokal != v1:
                                            hasil_line[idx1] = new_vokal

                elif met1 == '⏑' and v1_lower_temp in VOWEL_PANJANG:
                    kata_v1 = next((k for k in kata_list if k[0] <= idx1 < k[1]), None)
                    if kata_v1:
                        kata = kata_v1[2]
                        idx_rel = idx_vokal - kata_v1[0]
                        if idx_rel == len(kata) - 1:
                            next_kata_idx = kata_list.index(kata_v1) + 1
                            if next_kata_idx < len(kata_list):
                                next_kata = kata_list[next_kata_idx][2]
                                if len(next_kata) == 2 and RE_KONSONAN.match(next_kata[0]) and RE_VOKAL.match(next_kata[1]):
                                    if next_kata[0].lower() not in KHUSUS_KONSONAN:
                                        new_vokal = ubah_vokal_sesuai_metrum(v1, met1) # is_first_char=False di sini
                                        if new_vokal != v1:
                                            hasil_line[idx1] = new_vokal

            kata_v = next((k for k in kata_list if k[0] <= idx_vokal < k[1]), None)

            if kata_v:
                kata = kata_v[2]
                idx_rel = idx_vokal - kata_v[0]

                konsonan_sebelum = idx_rel > 0 and RE_KONSONAN.match(kata[idx_rel - 1])

                if (konsonan_sebelum and
                    idx_rel + 2 < len(kata) and
                    RE_KONSONAN.match(kata[idx_rel + 1]) and
                    RE_VOKAL.match(kata[idx_rel + 2])):

                    new_vokal = ubah_vokal_sesuai_metrum(vokal, metrum_vokal) # is_first_char=False di sini
                    if new_vokal != vokal:
                        hasil_line[idx_vokal] = new_vokal

        # --- LOGIKA PENGECEKAN KONSONAN GANDA (DIKONTROL OLEH TOGGLE) ---
        if ENABLE_KONSONAN_GANDA_CHECK:
            current_line_str_after_mod = ''.join(hasil_line)
            temp_clean_line_for_vowels = bersihkan_karakter_tak_terlihat(current_line_str_after_mod)
            re_vokal_posisi_in_original_line = []
            temp_clean_idx = 0
            temp_orig_idx = 0
            temp_clean_vokal_idx = 0

            temp_vokal_posisi_clean = []
            for idx, char in enumerate(temp_clean_line_for_vowels):
                if char.lower() in VOWELS:
                    temp_vokal_posisi_clean.append(idx)

            while temp_clean_idx < len(temp_clean_line_for_vowels) and temp_clean_vokal_idx < len(temp_vokal_posisi_clean):
                if temp_clean_idx == temp_vokal_posisi_clean[temp_clean_vokal_idx]:
                    while temp_orig_idx < len(current_line_str_after_mod):
                        if current_line_str_after_mod[temp_orig_idx].lower() in VOWELS:
                            metrum_idx = temp_clean_vokal_idx % len(selected_metrum)
                            re_vokal_posisi_in_original_line.append((temp_orig_idx, current_line_str_after_mod[temp_orig_idx], selected_metrum[metrum_idx]))
                            temp_orig_idx += 1
                            break
                        temp_orig_idx += 1
                    temp_clean_vokal_idx += 1
                temp_clean_idx += 1

                while temp_orig_idx < len(current_line_str_after_mod) and (current_line_str_after_mod[temp_orig_idx] == ZWNJ or current_line_str_after_mod[temp_orig_idx] == ZWJ):
                    temp_orig_idx += 1

            for i_vokal_curr, (idx_vokal, vokal, metrum_vokal) in enumerate(re_vokal_posisi_in_original_line):
                vokal_lower = vokal.lower()

                if vokal_lower in VOWELS and metrum_vokal == '⏑':
                    if i_vokal_curr + 1 < len(re_vokal_posisi_in_original_line):
                        idx_next_vokal_orig = re_vokal_posisi_in_original_line[i_vokal_curr + 1][0]

                        # Ambil substring antara vokal saat ini dan vokal berikutnya di *clean_line_for_vowels*
                        # Ini penting agar indeks karakter sesuai dengan yang ada di clean_line_for_vowels
                        start_clean_idx = next((i for i, (o_idx, _, _) in enumerate(vokal_posisi_in_original_line) if o_idx == idx_vokal), -1)
                        end_clean_idx = next((i for i, (o_idx, _, _) in enumerate(vokal_posisi_in_original_line) if o_idx == idx_next_vokal_orig), -1)

                        if start_clean_idx == -1 or end_clean_idx == -1:
                            continue # Should not happen if vokal_posisi_in_original_line is correctly built

                        # Dapatkan indeks di `temp_clean_line_for_vowels`
                        idx_vokal_clean = temp_vokal_posisi_clean[start_clean_idx]
                        idx_next_vokal_clean = temp_vokal_posisi_clean[end_clean_idx]

                        substring_between_vowels_clean = temp_clean_line_for_vowels[idx_vokal_clean + 1 : idx_next_vokal_clean]

                        konsonan_count_between = 0

                        # Loop melalui karakter di substring yang bersih
                        j = 0
                        while j < len(substring_between_vowels_clean):
                            char = substring_between_vowels_clean[j]

                            if RE_KONSONAN.match(char.lower()) and char != '-':
                                konsonan_count_between += 1 
                            j += 1

                        if konsonan_count_between > 1:
                            current_line_has_error_marker = True
                            kata_terkait = next((k[2] for k in kata_list if k[0] <= idx_vokal < k[1]), None)
                            if kata_terkait:
                                current_line_error_message = f'"{bersihkan_karakter_tak_terlihat(kata_terkait)}"'
                            else:
                                error_substring_for_msg = bersihkan_karakter_tak_terlihat(substring_between_vowels_clean)
                                current_line_error_message = f'"{error_substring_for_msg}"'
                            break

        final_line_output = ''.join(hasil_line)

        # --- Normalisasi Akhir untuk ṝḹṛḷ ---
        # Mengembalikan karakter kapitalisasi khusus ke bentuk lowercase-nya
        for old_char, new_char in FINAL_NORMALIZATION_MAP.items():
            final_line_output = final_line_output.replace(old_char, new_char)

        final_clean_line = bersihkan_karakter_tak_terlihat(final_line_output)
        final_vokal_count = sum(1 for char in final_clean_line if char.lower() in VOWELS)

        metrum_length_for_line = len(selected_metrum)

        plus_minus_indicator = ""
        if metrum_length_for_line > 0:
            if final_vokal_count > metrum_length_for_line:
                plus_minus_indicator = f'"+{final_vokal_count - metrum_length_for_line}"'
            elif final_vokal_count < metrum_length_for_line:
                plus_minus_indicator = f'"–{metrum_length_for_line - final_vokal_count}"'

        if current_line_has_error_marker or plus_minus_indicator:
            error_details = []
            if current_line_error_message:
                error_details.append(current_line_error_message)
            if plus_minus_indicator:
                error_details.append(plus_minus_indicator)

            error_string = " | ".join(error_details)
            processed.append(f"{final_line_output}{' ' * JARAK_TANDA_SALAH}{TANDA_SALAH} {error_string}")
        else:
            processed.append(final_line_output)
    return processed


def aplikasikan_metrum_dan_tandai_vokal(text):
    """
    Fungsi utama untuk mengaplikasikan metrum dan menandai vokal pada text puisi.
    """
    blok_list = re.split(r'\n\s*\n', text.strip(), flags=re.MULTILINE)
    hasil_blok = []
    current_metrum = []

    for blok in blok_list:
        baris = blok.strip().splitlines()
        is_metrum_blok = any(RE_METRUM_SIMBOL.search(b) for b in baris)
        header_blok = [b for b in baris if (b.startswith("<") and ">" in b) or #penanda sargah/pupuh utama
                                           (b.startswith("{") and "}" in b) or #penanda sub pupuh
                                           (b.startswith("]") and "]" in b) or
                                           (b.startswith("[") and "[" in b) or
                                           (b.startswith("!") and "!" in b) or #penanda wirama yang tidak diketahui 
                                           (b.startswith("#") and b.endswith("#"))]
        puisi_baris = [b for b in baris if not RE_METRUM_SIMBOL.search(b) and
                                           not (b.startswith("<") and ">" in b or
                                                b.startswith("{") and "}" in b or
                                                b.startswith("]") and "]" in b or
                                                b.startswith("[") and "[" in b or
                                                b.startswith("!") and "!" in b or
                                                b.startswith("#") and b.endswith("#"))]
        metrum_baris_temp = [get_clean_metrum(b) for b in baris if RE_METRUM_SIMBOL.search(b)]

        hasil_blok.extend(header_blok)

        if is_metrum_blok:
            current_metrum = metrum_baris_temp
            hasil_blok.extend([b for b in baris if RE_METRUM_SIMBOL.search(b)])
        elif current_metrum:
            jumlah_metrum_metrum_blok = len(current_metrum)
            processed_puisi = []
            
            for idx_line, line_puisi in enumerate(puisi_baris):
                metrum_for_this_line = [current_metrum[idx_line % jumlah_metrum_metrum_blok]]
                processed_line_from_buffer = proses_puisi_buffer([line_puisi], metrum_for_this_line)
                processed_puisi.extend(processed_line_from_buffer)

            hasil_blok.extend(processed_puisi)
        else:
            hasil_blok.extend(puisi_baris)

        hasil_blok.append("")

    return "\n".join(hasil_blok).strip()

def cek_kakawin(text):
    """
    Fungsi ini memproses text puisi untuk menandai vokal pendek yang berada dalam
    pasangan dengan vokal pendek lainnya dalam satu kata, sesuai dengan aturan metrum.
    Fungsi ini juga menghitung jumlah metrum pada baris metrum dan menandai
    ketidaksesuaian antara jumlah vokal dan simbol metrum.
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
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                if metrum_lines:
                    hasil_blok.extend(metrum_lines)
                    metrum_lines = []
                hasil_blok.append(line)
                current_metrum = []
            elif line.startswith("{") and "}" in line: 
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                if metrum_lines:
                    hasil_blok.extend(metrum_lines)
                    metrum_lines = []
                hasil_blok.append(line)
                current_metrum = []
            elif line.startswith("]") and "]" in line: 
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                if metrum_lines:
                    hasil_blok.extend(metrum_lines)
                    metrum_lines = []
                hasil_blok.append(line)
                current_metrum = []
            elif line.startswith("[") and "[" in line: 
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                if metrum_lines:
                    hasil_blok.extend(metrum_lines)
                    metrum_lines = []
                hasil_blok.append(line)
                current_metrum = []
            elif line.startswith("!") and line.endswith("!"):
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                if metrum_lines:
                    hasil_blok.extend(metrum_lines)
                    metrum_lines = []
                hasil_blok.append(line)
                current_metrum = []
            elif line.startswith("#") and line.endswith("#"):
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
                if puisi_buffer:
                    processed = proses_puisi_buffer(puisi_buffer, current_metrum)
                    hasil_blok.extend(processed)
                    puisi_buffer = []
                jumlah = hitung_jumlah_metrum(line)
                metrum_line = f"{line} = {jumlah}"
                metrum_lines.append(metrum_line)
                current_metrum.append(get_clean_metrum(line))
            else:
                puisi_buffer.append(line)
        if metrum_lines:
            hasil_blok.extend(metrum_lines)
        if puisi_buffer:
            processed = []
            if current_metrum:
                jumlah_metrum_metrum_blok = len(current_metrum)
                for idx_line, line_puisi in enumerate(puisi_buffer):
                    metrum_for_this_line = [current_metrum[idx_line % jumlah_metrum_metrum_blok]]
                    processed_line_from_buffer = proses_puisi_buffer([line_puisi], metrum_for_this_line)
                    processed.extend(processed_line_from_buffer)
            else:
                processed = puisi_buffer
            
            hasil_blok.extend(processed)
        hasil_blok.append("")
    hasil_akhir = "\n".join(hasil_blok).strip()
    return hasil_akhir