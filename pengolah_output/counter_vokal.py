def hitung_vokal(baris):
    vokal = 'aiueoĀāĪīŪūĔĕÊêÔôÉéÈèĚěOōUūĪīŌōâîêôöûâî'
    jumlah = sum(1 for huruf in baris if huruf.lower() in vokal.lower())
    return jumlah

# Contoh pemakaian:
baris = "mapa kālah-alah apa tāmbĕha tambulāsiṅ kakuraṅ kurawuṅ kurapas kurahan hana maṇḍaga riṅ raga sugwan ĕmās wwara piṇḍaṅ apiṇḍa lawan bakasêm pakasaṅśaya haywa tamuy-tamuyan yan asömasi wantĕna saṅgiṅ irāhira hèrakĕnā sakarĕṅ mwaṅ arīṅa-riṅan iriṅĕn tĕka dé niṅ ator sahajān hibĕki inuman tan umāna tĕkèṅ mawĕrö wwara hantiga lumwaṅalap gĕtĕm apya mapāta rasa nya rasénisi sisyanikā inamĕr nira saṅ walakas lĕkasan magaway rasa bhaṅgi wibhāga nikaṅ guṇabhoga tamar tama tā dadi bhaṅga r-usir subhago matakut kuyaśā-kuyaśa ṅ makarī sakarĕṅ makarā-kirakĕn ta ya siṅ matasak matasé kahiris ta harah kuya taṅĕli pawĕhaṅkĕn osen-usĕn nda hanus hunus īku pinaṅgaṅakĕn taṅ ikān putih antĕr i ḍatĕṅ ndan ahaywa ḍatĕṅ walikāpĕs-apĕs mwas ikā hati niṅ hyu lawan pya ṇikaṅ hawulāmrak inaṅsi ṅ usīra pasāra ya satwa śaśā wana kurkuṭa ugra rasottama tad warahĕn n irikaṅ hitamāṅsa hanĕṅ aji sūpakaśāstra milu ṅ lulu kambiṅ anuṅ maharĕṅ wayawak ruti wūru-wurū prit awor puyuh uttama"
print("Jumlah vokal:", hitung_vokal(baris))