def hitung_vokal(baris):
    vokal = 'aiueoĀāĪīŪūĔĕÊêÔôÉéÈèĚěOōUūĪīŌōâîêôöûâî'
    jumlah = sum(1 for huruf in baris if huruf.lower() in vokal.lower())
    return jumlah

# Contoh pemakaian:
baris = "jalak ajar-ajaran bayan syuṅ puyuh kwèh pĕjah mungu rin pañjaré pañcaraṅkaṅ hĕmas tan katolih alah mrih awak nyêkanaṅ rākṣasi śīghra luṅhā hah-āh-āh-āh liṅ nya kapwāmĕhāh yāṅuhuh mohitān ton ikaṅ rākṣasomèh tibā riṅ apuy mogha momo umèh mātya ya"
print("Jumlah vokal:", hitung_vokal(baris))