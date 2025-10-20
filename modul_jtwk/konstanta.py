# --- Variabel Global ---
ZWNJ = '\u200C'
ZWSP = '\u200B'
ZWJ = '\u200D'
ZWNBSP = '\uFEFF'
SH = '\u00AD' #soft hypen
DAFTAR_KONSONAN = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅṙṛṝḷḹꝁǥꞓƀśḳkʰ"
DAFTAR_VOKAL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûôAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOKAL_KAPITAL = "AĀÂIĪÎUŪÛOŌÔEĔÊÉÈꜼꜶ"
VOKAL_NON_KAPITAL = 'aāiīuūeèéêoōöŏĕꜷꜽâîûô'
VOKAL_NON_KAPITAL_REGEX = f"[{VOKAL_NON_KAPITAL}]"
SEMI_VOKAL = 'lwyr'
TIDAK_DIGANDAKAN = set('nṅṇhṣsścꞓrṙṫŧꝑǥɉƀꝁkdḍḋdđfv')

#Untuk kakawin
VOKAL_PANJANG = 'āâîīûūêôeèéöoōŏꜽꜷĀÂÎĪÛŪÊŎÔŌṝḹ'