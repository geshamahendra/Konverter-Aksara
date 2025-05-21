def hitung_vokal(baris):
    vokal = 'aiueoĀāĪīŪūĔĕÊêÔôÉéÈèĚěOōUūĪīŌōâîêôöûâî'
    jumlah = sum(1 for huruf in baris if huruf.lower() in vokal.lower())
    return jumlah

# Contoh pemakaian:
baris = "jalak ajar-ajaran bayan syuṅ puyuh kwèh pĕjah muṅgu rin pañjaré pañcaraṅkaṅ hĕmas tan katon tan katolih alah mrih awak nyêkanaṅ rākṣasī śīghra luṅhā hah-āh-āh-āh liṅ nya kapwāmĕhāh yāṅuhuh mohitān ton ikaṅ rākṣasa umèh tibā riṅ apuy mogha momo umèh mātya ya"
print("Jumlah vokal:", hitung_vokal(baris))