def hitung_vokal(baris):
    vokal = 'aiueoĀāĪīŪūĔĕÊêÔôÉéÈèĚěOōUūĪīŌōâîêôöûâîꜽꜷ'
    jumlah = sum(1 for huruf in baris if huruf.lower() in vokal.lower())
    return jumlah

# Contoh pemakaian:
baris = "ṅuni-ṅuni yan ikaṅ musuh mātya niĕśéṣa dèntêṅ raṇa byakta homanta méman tĕmen tat t-amètā byayantāṅhīṅ ikāṅĕn-āṅĕn nikāṅĕn-n-aṅĕntā-lilaṅ nitya saṅ hyaṅ Mahāwirabhadréśwarālambanānèṅ raṇāṅgāṅgaṇāniṅ pahoman samiddhānta waṅkay nikaṅ śatru sampūrṇna pūrṇnahuti rāh utĕk"
print("Jumlah vokal:", hitung_vokal(baris))