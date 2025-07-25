import re

def normalisasi_vokal(char):
    char_lower = char.lower()
    if re.match(r'[aāâ]', char_lower):
        return 'a'
    elif re.match(r'[iīî]', char_lower):
        return 'i'
    elif re.match(r'[uūû]', char_lower):
        return 'u'
    elif re.match(r'[eêéèꜼꜶ]', char_lower):
        return 'e'
    elif re.match(r'[oōöŏoꜽꜷ]', char_lower):
        return 'o'
    elif re.match(r'[ĕ]', char_lower):
        return 'ĕ'
    else:
        return ""

def hitung_vokal(baris):
    jumlah = 0
    for char in baris:
        if normalisasi_vokal(char):
            jumlah += 1
    return jumlah

def cek_macapat(text):
    blok = text.strip().split('\n')
    hasil = []
    kamus_aturan = {
        "sinom": ["8a", "8i", "8a", "8i", "7i", "8u", "7a", "8i", "12a"],
        "mĕgatruꞕ": ["12u", "8i", "8u", "8i", "8o"],
        "lindur": ["10u", "8i", "8i", "8a", "6i", "8a", "6i", "6a", "6i", "6i", "6i"],
        "dhandhanggula": ["10i", "10a", "8e/o", "7u", "9i", "7a", "6u", "8a", "12i", "7a"], # Tambahan Dhandhanggula
        "kĕnya kadhiri": ["12u", "8i", "12u", "12u", "12u", "8i", "8i", "6u", "8i"],
        "asmara dana": ["8i", "8a", "8i", "7i", "8u", "7a", "8i", "12a"],
        "durma": ["12a", "7i", "6a", "7a", "8i", "5a", "7i"],
        "gurawa": ["9a", "8i", "7a", "8a", "8i", "4/5/6a", "8i"], # Perhatikan 4/5/6a
        "jurudĕmung": ["8a", "8u", "8u", "8u", "8a", "8u", "8a"],
        "girisa": ["8a", "8a", "8a", "8a", "8a", "8a", "8a"],
        "kulante": ["6e", "6e", "8e", "8u", "8i", "8e", "8i", "12e"],
        "panji-prakasa": ["8i", "8i", "8i", "8i", "8a", "8u", "7i", "8i"],
        "sumekar": ["4a", "8i", "8a", "8a", "8i", "4a", "6e"],
        "pangkur": ["8a", "11i", "8u", "7a", "12u", "8a", "8i"],
        "salobok": ["8i", "8a", "8o", "7a", "7a", "8u", "8a"],
        "balabak/bĕlabak": ["12a", "3e", "12a", "3e", "12a", "3e"],
        "kinanthi": ["8u", "8i", "8a", "8i", "8a", "8i"],
        "mijil": ["10i", "6o", "10e", "10i", "6i", "6u"],
        "pamijil": ["10i", "6e", "10e", "10i", "6i", "6u"],
        "miring": ["12i", "3a", "12i", "3a", "12i", "3a"],
        "wirangrong": ["8i", "8o", "10u/a", "6a", "6i/10i", "7a", "8a"], # Perhatikan 10u/a dan 6i/10i
        "name unknown": ["8e", "7a", "8o", "9a", "8e"],
        "darmaparita": ["8a", "8a", "12e", "7i", "12e"],
        "gambuh": ["7/8u", "10/12u", "12u", "8u", "8o"], # Perhatikan 7/8u dan 10/12u
        "maesa langit": ["9e(?)", "7u", "8i(?)", "8u", "8o(?)", "40"], # Perhatikan (?)
        "kinanthi jugag": ["8u", "8a", "8a", "8a"],
        "kulawarnat": ["12u", "8a", "12a"],
        "ladrang": ["12i", "4a", "8i", "12a"],
        "maskumambang": ["12i", "6a", "8i", "8a"],
        "warti": ["12i", "8a", "8i", "8a"],
        "pocung": ["12u (4u, 8u)", "6a", "8i/o/e/o", "12a"], # Perhatikan (4u, 8u) dan 8i/o/e/o
        "salisir": ["8a", "8a", "8a", "8a"],
        "lonthang": ["12a", "12a", "12a"]
    }
    
    # Menambah pola regex untuk mendeteksi apakah ini blok metrum
    pola_metrum = re.compile(r'^\s*[<{\[]([^>}\]]+)[>}\]]\s*$')
    
    # Variabel untuk pelacakan status
    metrum_aktif = None
    aturan_aktif = None
    stanza_aktif = []  # Untuk melacak baris-baris dalam satu stanza
    
    # Proses setiap baris dalam input
    i = 0
    while i < len(blok):
        baris = blok[i].strip()
        
        # Identifikasi blok metrum
        match_metrum = pola_metrum.match(baris)
        if match_metrum:
            # Jika ini adalah penanda metrum baru
            nama_metrum = match_metrum.group(1).strip()
            
            # Tambahkan baris metrum ke hasil
            hasil.append(baris)
            
            # Set metrum aktif jika dikenali
            if nama_metrum in kamus_aturan:
                metrum_aktif = nama_metrum
                aturan_aktif = kamus_aturan[nama_metrum]
            else:
                metrum_aktif = None
                aturan_aktif = None
                
            # Reset stanza aktif untuk metrum baru
            stanza_aktif = []
            i += 1
            continue
        
        # Jika baris kosong, ini penanda stanza baru
        if not baris and metrum_aktif:
            # Reset stanza aktif untuk stanza baru
            stanza_aktif = []
            hasil.append("")  # Tambahkan baris kosong ke hasil
            i += 1
            continue
        
        # Proses baris puisi jika ada metrum aktif
        if baris and metrum_aktif and aturan_aktif:
            # Tambahkan baris ke stanza aktif
            stanza_aktif.append(baris)
            
            # Tentukan posisi dalam pola metrum
            posisi_baris = (len(stanza_aktif) - 1) % len(aturan_aktif)
            
            # Dapatkan aturan untuk baris ini
            aturan = aturan_aktif[posisi_baris]
            
            # --- MODIFIKASI DIMULAI DI SINI ---
            
            # Pola regex untuk mengekstrak jumlah suku kata dan vokal target
            # Akan mengenali: "8a", "8i/o/e", "12u (4u, 8u)", "7/8u"
            match_aturan = re.match(r'(\d+)(?:/(\d+))?\s*(?:(?:\(|\s)([a-zA-Z\/]+)(?:\)))?([a-zA-Z\/]*)', aturan)

            jumlah_target = []
            vokal_target_list = []
            
            if match_aturan:
                # Ambil jumlah suku kata pertama
                jumlah_target.append(int(match_aturan.group(1)))
                # Jika ada jumlah suku kata kedua (misal: 7/8u)
                if match_aturan.group(2):
                    jumlah_target.append(int(match_aturan.group(2)))

                # Ambil vokal target dari grup 3 (misal: 8i/o/e/o) atau grup 4 (misal: 8a)
                if match_aturan.group(3):
                    vokal_part = match_aturan.group(3)
                else:
                    vokal_part = match_aturan.group(4)

                # Pisahkan vokal target jika ada '/'
                if vokal_part:
                    vokal_target_list = [v.lower() for v in vokal_part.split('/') if v]
                
                # Menambahkan vokal dalam kurung jika ada (misal: 12u (4u, 8u))
                # Note: Untuk kasus (4u, 8u), ini tidak langsung menjadi vokal target, 
                # melainkan sub-pola. Kode ini hanya fokus pada guru lagu akhir.
                # Penanganan untuk sub-pola ini akan lebih kompleks dan mungkin memerlukan
                # parsing terpisah jika Anda ingin memvalidasi setiap bagian dalam kurung.
                # Untuk saat ini, kita hanya fokus pada vokal akhir dari bagian utama.
            
            # Tangani kasus khusus seperti "9e(?)" atau "8i(?)"
            if not vokal_target_list and '?' in aturan:
                # Jika ada '?' dan tidak ada vokal target yang teridentifikasi,
                # kita bisa anggap vokal ini tidak bisa divalidasi atau abaikan validasi vokal untuk baris ini.
                # Untuk contoh ini, kita akan melewati validasi vokal untuk baris ini jika hanya ada '?'
                pass # Lanjut ke validasi jumlah suku kata saja jika ada
            elif not vokal_target_list:
                 # Jika tidak ada vokal target yang terdeteksi, ini mungkin format yang tidak didukung
                 # atau kesalahan dalam aturan kamus. Untuk POCUNG, '12u (4u, 8u)'
                 # vokal targetnya adalah 'u'. Kita harus lebih spesifik.
                 # Jika tidak ada vokal yang teridentifikasi dari regex, coba ambil karakter terakhir
                 # selama itu adalah huruf. Ini akan menangani "12a" atau "8o"
                 last_char_aturan = aturan.strip()[-1].lower()
                 if last_char_aturan.isalpha() and last_char_aturan in ['a', 'i', 'u', 'e', 'o', 'ĕ']:
                     vokal_target_list = [last_char_aturan]


            # --- MODIFIKASI BERAKHIR DI SINI ---
            
            # Hitung jumlah vokal
            jumlah_vokal = hitung_vokal(baris)
            
            # Cari vokal akhir
            vokal_akhir = ""
            for char in reversed(baris):
                normalized = normalisasi_vokal(char)
                if normalized:
                    vokal_akhir = normalized.lower()
                    break
            
            # Periksa apakah sesuai aturan
            # Validasi jumlah suku kata
            jumlah_valid = False
            if not jumlah_target: # Jika tidak ada target jumlah, mungkin format aturan tidak dikenali
                jumlah_valid = False # Atau bisa juga True jika ingin membiarkannya
            elif len(jumlah_target) == 1:
                jumlah_valid = (jumlah_vokal == jumlah_target[0])
            else: # Untuk kasus 7/8u, 4/5/6a
                jumlah_valid = (jumlah_vokal in jumlah_target)

            # Validasi vokal akhir
            vokal_valid = False
            if not vokal_target_list: # Jika tidak ada vokal target yang didefinisikan (misal: "9e(?)")
                vokal_valid = True # Anggap valid untuk vokal akhir
            else:
                vokal_valid = (vokal_akhir in vokal_target_list)

            # Kondisi gabungan untuk error
            if not jumlah_valid or not vokal_valid:
                pesan_error_guru_wilangan = ""
                if not jumlah_valid:
                    if len(jumlah_target) == 1:
                        pesan_error_guru_wilangan = f"sĕharusnya {jumlah_target[0]} suku kata"
                    else:
                        pesan_error_guru_wilangan = f"sĕharusnya {', '.join(map(str, jumlah_target))} suku kata"

                pesan_error_guru_lagu = ""
                if not vokal_valid and vokal_target_list: # Hanya tambahkan jika ada vokal target yang diharapkan
                    pesan_error_guru_lagu = f"guru lagu '{'/'.join(vokal_target_list)}'"
                
                pesan_error = ""
                if pesan_error_guru_wilangan and pesan_error_guru_lagu:
                    pesan_error = f"({pesan_error_guru_wilangan}, {pesan_error_guru_lagu})"
                elif pesan_error_guru_wilangan:
                    pesan_error = f"({pesan_error_guru_wilangan})"
                elif pesan_error_guru_lagu:
                    pesan_error = f"({pesan_error_guru_lagu})"

                hasil.append(f"{baris} ❌ {pesan_error}")
            else:
                hasil.append(baris)
        else:
            # Jika tidak ada metrum aktif atau baris kosong, tambahkan apa adanya
            hasil.append(baris)
        
        i += 1
    
    return "\n".join(hasil)