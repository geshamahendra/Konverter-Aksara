import re

# --- Variabel Global ---
ZWNJ = '\u200C'
ZWSP = '\u200B'
ZWJ = '\u200D'
ZWNBSP = '\uFEFF'
SH = '\u00AD' #soft hypen
DAFTAR_KONSONAN = "bcdfghjɉklmnpqrstvwyzḋḍđŧṭṣñṇṅꝁǥꞓƀśḳkʰḥṙŋᶉꞕᶇ"
DAFTAR_VOKAL = 'ṛṝḷḹaāiīuūeèéêoōöŏĕꜷꜽâîûôAĀÂIĪÎUŪÛOŌÔEÊÉÈꜼꜶ'
VOKAL_KAPITAL = "AĀÂIĪÎUŪÛOŌÔEĔÊÉÈꜼꜶ"
VOKAL_NON_KAPITAL = 'ṛṝḷḹaāiīuūeèéêoōöŏĕꜷꜽâîûô'
VOKAL_NON_KAPITAL_REGEX = f"[{VOKAL_NON_KAPITAL}]"
SEMI_VOKAL = 'lwyr'
TIDAK_DIGANDAKAN = set('nṅṇhṣsścꞓrṙṫŧꝑǥɉƀꝁkdḍḋdđfv')

#hukum_kakawin
# --- Regex dan Konstanta Lainnya ---
RE_METRUM_SIMBOL = re.compile(r'[—⏑⏓]')
RE_VOKAL = re.compile(r'[aiuĕāâîīûūêôeèéōöŏoꜽꜷAĀÂIĪÎUŪÛOŎŌÔEÊÉÈꜼꜶṝḹṛḷ❓]')
RE_KONSONAN = re.compile(r'[bcdfghjɉklmnpꝑqrstvwyzḋḍđŧṭṣñṇṅꝁǥꞓƀśḳʰ–]') #en-dash
ZWNJ = '\u200C'
ZWJ = '\u200D'
# Definisi ṝḹṛḷ sebagai vokal
VOWELS = 'aiuĕāâîīûūêôeèéöëoōŏꜽꜷAIUĀÂÎĪÛŪÊŎÔŌꜼꜶṚḶṜḸṝḹṛḷ❓'
VOKAL_PENDEK = 'aiuĕAIUĔṚṛḶḷ❓'
VOKAL_PANJANG = 'āâîīûūêôeèéëöoōŏꜽꜷĀÂÎĪÛŪÊŎÔŌꜼꜶṜṝḸḹ'
KHUSUS_KONSONAN = 'ŋḥṙṃ'