import re

def stabilkan_spasi_metrum(teks):
    def pisahkan_simbol(match):
        simbol = match.group(0)
        return ' '.join(simbol)
    return re.sub(r'[⏑–⏓|]+', pisahkan_simbol, teks)

def renumber_canto(text):
    lines = text.splitlines()
    nomor1 = 0
    nomor2 = 0
    nomor3 = 0
    output = []

    tunggu_bait_pertama = False
    gt_keberapa = 0

    for idx, line in enumerate(lines):
        if re.search(r'>', line):
            nomor1 += 1
            nomor2 = 0
            gt_keberapa += 1
            tunggu_bait_pertama = True
            output.append(line)
            continue

        if tunggu_bait_pertama:
            # Lewati baris kosong atau baris metrum
            if line.strip() == '' or re.search(r'[⏑–⏓]', line):
                output.append(line)
                continue
            else:
                prefix = '%' if gt_keberapa == 1 else '^'
                line = prefix + line
                tunggu_bait_pertama = False

        # Penomoran akhir jika baris diakhiri *
        if line.strip().endswith('*'):
            nomor2 += 1
            nomor3 += 1
            line = re.sub(r'\*+$', '', line) + f"*{nomor1}:{nomor2}:{nomor3}*"

        output.append(line)

    result = '\n'.join(output)
    result = re.sub(r'(,)\n', r'\1', result)
    result = re.sub(r'>(.*\n.*\n.*.*\n.*)(\*)(\d+)(:)(\d+:\d+.*)', r'>:\3\1\2\3\4\5', result)
    result = stabilkan_spasi_metrum(result)
    #result = re.sub(r'^\d.*\n', r'', result)
    return result

# Uji coba
with open("pengolah_output/input_lontar.txt", "r", encoding="utf-8") as f:
    teks = f.read()

hasil = renumber_canto(teks)
hasil = re.sub(r'\n(\d.*\n)', r'\n', hasil)
hasil = re.sub(r'(\*)\n\n(\w)', r'\1\2', hasil)


with open("pengolah_output/output_lontar.txt", "w", encoding="utf-8") as f:
    f.write(hasil)
