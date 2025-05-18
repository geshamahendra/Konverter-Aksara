import re

def stabilkan_spasi_metrum(teks):
    # Fungsi ini akan mengganti semua rangkaian simbol metrum tanpa spasi menjadi versi dipisah spasi
    def pisahkan_simbol(match):
        simbol = match.group(0)
        return ' '.join(simbol)

    # Regex untuk semua kelompok karakter metrum tanpa campuran huruf lain
    return re.sub(r'[⏑–⏓|]+', pisahkan_simbol, teks)

def renumber_canto(text):
    lines = text.splitlines()
    nomor1 = 0
    nomor2 = 0
    nomor3 = 0
    output = []

    for i, line in enumerate(lines):
        if re.search(r'>', line):
            nomor1 += 1
            nomor2 = 0
            output.append(line)
            continue

        if line.strip() == '' and i + 1 < len(lines) and lines[i + 1].strip().endswith(','):
            nomor2 += 1
            nomor3 += 1
            output.append(line)
            output.append(f"{nomor1}/{nomor2}/{nomor3}.")
            continue

        output.append(line)

    result = '\n'.join(output)

    # Hapus baris kosong tepat sebelum baris yang mengandung /1/
    result = re.sub(r'\n\s*\n(?=.*?/1/)', r'\n', result)

    # Stabilkan spasi antar simbol metrum
    result = stabilkan_spasi_metrum(result)

    return result

# Uji coba
with open("pengolah_output/input_pupuh.txt", "r", encoding="utf-8") as f:
    teks = f.read()

hasil = renumber_canto(teks)

with open("pengolah_output/output_pupuh.txt", "w", encoding="utf-8") as f:
    f.write(hasil)
