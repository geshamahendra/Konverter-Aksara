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
        "mĕgatruꞕ": ["12u", "8i", "8u", "8i", "8o"]
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
            jumlah_target = int(aturan[:-1])
            vokal_target = aturan[-1].lower()  # Pastikan lowercase untuk perbandingan
            
            # Hitung jumlah vokal
            jumlah_vokal = hitung_vokal(baris)
            
            # Cari vokal akhir
            vokal_akhir = ""
            for char in reversed(baris):
                normalized = normalisasi_vokal(char)
                if normalized:
                    vokal_akhir = normalized.lower()  # Pastikan lowercase untuk perbandingan
                    break
            
            # Periksa apakah sesuai aturan
            if jumlah_vokal != jumlah_target or vokal_akhir != vokal_target:
                pesan_error = f"❌ (baris-:{posisi_baris+1}:, sĕharusnya :{jumlah_target}: suku kata, guru lagu ':{vokal_target}:') "
                hasil.append(f"{baris} {pesan_error}")
            else:
                hasil.append(baris)
        else:
            # Jika tidak ada metrum aktif atau baris kosong, tambahkan apa adanya
            hasil.append(baris)
        
        i += 1
    
    return "\n".join(hasil)