import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
# Pastikan jalur ini benar untuk struktur proyek Anda
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# --- IMPOR MODUL DAN FUNGSI ANDA ---
try:
    from jtwk_ke_jawa import latin_to_jawa
    from latin_ke_jtwk import replace_characters
    from jawa_ke_bali import konversi_aksara_ke_bali
    from jawa_ke_kawi import konversi_aksara_ke_kawi
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Pastikan modul ada di direktori yang benar dan berisi file-file yang diperlukan.")
    sys.exit(1)

# --- DEFINISI ATURAN REGEX SPESIFIK FONT YANG BERBAGI ---
# Definisikan set aturan regex yang umum atau sering digunakan
# Ini membuat FONT_SPECIFIC_REGEX_RULES lebih bersih dan mudah dikelola
WASKITA_RULES = [
    (r'ꦪꦾꦂ', 'ꦫ꧀ꦪꦾ'),
    (r'ꦫ꧀ꦮ', 'ꦫ꧀ꦮ\u200D'), # Tambahkan Zero-Width Joiner (ZWJ) untuk penyambungan yang lebih baik
    #(r'ꦂ', 'ꦂ\u200D', re.IGNORECASE) # Tambahkan ZWJ setelah pangkon (ꦂ)
    (r'ꦂ', 'ꦫ꧀', re.IGNORECASE) # Tambahkan ZWJ setelah pangkon (ꦂ)
]
GAYATRI_RULES = [
    (r'ꦈ', '#'),
    (r'ꦎ', 'ꦈ'),
    (r'#', 'ꦎ'),
    (r'ꦪꦾꦂ', 'ꦫ꧀ꦪꦾ'),
    (r'ꦫꦾ', '꧟'),
    (r'ꦫ꧀ꦮ\u200c', '꧞'),
    (r'ꦾ', '꧀ꦪ'),
    (r'ꦿ', '꧀ꦫ'),
    (r'ꦂ', 'ꦂ', re.IGNORECASE)#layar ke layar
] # Aturan untuk font Vimala (saat ini kosong, tambahkan jika diperlukan)

# Jika ada aturan umum lain untuk Bali, Kawi, atau font lain, definisikan di sini.
# Contoh:
# VIMALA_BALI_RULES = [
#     (r'aturan_khusus_vimala_bali_1', 'pengganti_1'),
#     (r'aturan_khusus_vimala_bali_2', 'pengganti_2'),
# ]

# --- DEFINISI ATURAN REGEX SPESIFIK FONT ---
# Dictionary ini menyimpan aturan regex yang perlu diterapkan untuk font tertentu
# Kunci: aksara_type -> font_family -> daftar_aturan (pattern, replacement, flags)
FONT_SPECIFIC_REGEX_RULES = {
    "jawa": {
        "jayabaya": WASKITA_RULES, # Referensikan set aturan yang sudah didefinisikan
        "Asta Gayatri 09": GAYATRI_RULES, # Aturan untuk font Vimala (saat ini kosong)
        "Simbar Dwijendra 2": []                       # Aturan untuk font Simbar Dwijendra 2 (saat ini kosong)
    },
    "bali": {
        "vimala": [], # Contoh: VIMALA_BALI_RULES, # Jika ada, referensikan di sini
        "Simbar Dwijendra 2": []
    },
    "kawi": {
        "Noto Sans Kawi": [] # Aturan untuk font Jayabaya Aksara Kawi (saat ini kosong)
    }
}

def main_convertion(text, line_spacing, mode, aksara_type, font_family):
    """
    Fungsi konversi utama yang disesuaikan untuk berbagai jenis aksara dan font.
    """
    # Langkah 1: Proses awal teks Latin dan konversi ke Jawa
    text = replace_characters(text, mode)
    converted_jawa = latin_to_jawa(text, line_spacing)

    # Langkah 2: Konversi berdasarkan jenis aksara yang dipilih
    if aksara_type == "jawa":
        text_output = converted_jawa
        # Khusus untuk font Jayabaya, lakukan swap karakter ꦈ dan ꦎ menggunakan str.replace()
        # Ini menghindari masalah dengan re.sub dan karakter Unicode tertentu
        if font_family == "jayabaya":
            # Lakukan swap tiga arah
            text_output = text_output.replace('ꦈ', 'TEMP_JAYABAYA_U_PLACEHOLDER')
            text_output = text_output.replace('ꦎ', 'ꦈ')
            text_output = text_output.replace('TEMP_JAYABAYA_U_PLACEHOLDER', 'ꦎ')
    elif aksara_type == "bali":
        text_output = konversi_aksara_ke_bali(converted_jawa)
    elif aksara_type == "kawi":
        text_output = konversi_aksara_ke_kawi(converted_jawa)
    else:
        return "Pilihan aksara tidak valid."

    # Langkah 3: Terapkan manipulasi spesifik font (regex) jika ada
    # Cek apakah ada aturan regex yang didefinisikan untuk kombinasi aksara dan font ini
    if aksara_type in FONT_SPECIFIC_REGEX_RULES and \
       font_family in FONT_SPECIFIC_REGEX_RULES[aksara_type]:
        
        rules_to_apply = FONT_SPECIFIC_REGEX_RULES[aksara_type][font_family]
        for pattern, replacement, *flags in rules_to_apply:
            current_flags = flags[0] if flags else 0 # Ambil flags jika ada, default 0 (tidak ada flags)
            text_output = re.sub(pattern, replacement, text_output, flags=current_flags)
    
    return text_output

# --- FUNGSI UTAMA UNTUK INTERAKSI GUI ---
conversion_cache = {}
last_active_widget = None

def process_input(event=None):
    global last_active_widget
    current_text = input_text_widget.get("1.0", tk.END).strip()
    selected_aksara = aksara_var.get() # Ambil pilihan aksara
    selected_font_family = font_family_vars[selected_aksara].get() # Ambil pilihan font

    if not current_text:
        display_output_aksara("")
        return

    # Lakukan konversi berdasarkan pilihan aksara dan font
    converted_full_text = main_convertion(current_text, line_spacing=1, mode='lampah', 
                                          aksara_type=selected_aksara, font_family=selected_font_family)
    
    # Untuk aksara jawa, kita bisa hapus spasi jika diinginkan (ini adalah aturan umum, bukan font-spesifik)
    if selected_aksara == "jawa":
        final_output = converted_full_text.replace(" ", "")
    else:
        final_output = converted_full_text
        
    display_output_aksara(final_output)

    if event and (event.type == '2' or event.type == '4' or event.type == '6'):
        sync_cursors(event)

def display_output_aksara(text):
    output_aksara_widget.config(state=tk.NORMAL)
    output_aksara_widget.delete("1.0", tk.END)
    output_aksara_widget.insert("1.0", text)
    output_aksara_widget.config(state=tk.DISABLED)

# --- FUNGSI UNTUK SINKRONISASI KURSOR DENGAN HIGHLIGHT ---
def sync_cursors(event):
    active_widget = event.widget
    
    if not isinstance(active_widget, scrolledtext.ScrolledText):
        return

    current_line = int(active_widget.index(tk.INSERT).split('.')[0])
    
    other_widget = None
    if active_widget == input_text_widget:
        other_widget = output_aksara_widget
    elif active_widget == output_aksara_widget:
        other_widget = input_text_widget
    
    if other_widget:
        input_text_widget.tag_remove("highlight", "1.0", tk.END)
        output_aksara_widget.tag_remove("highlight", "1.0", tk.END)

        original_state_other = other_widget.cget("state")
        if original_state_other == tk.DISABLED:
            other_widget.config(state=tk.NORMAL)
        
        other_widget.mark_set(tk.INSERT, f"{current_line}.0")
        other_widget.see(tk.INSERT)

        start_index = f"{current_line}.0"
        end_index = f"{current_line}.end"
        
        input_text_widget.tag_add("highlight", start_index, end_index)
        output_aksara_widget.tag_add("highlight", start_index, end_index)

        root.after(1500, lambda: input_text_widget.tag_remove("highlight", start_index, end_index))
        root.after(1500, lambda: output_aksara_widget.tag_remove("highlight", start_index, end_index))

        if original_state_other == tk.DISABLED:
            other_widget.config(state=tk.DISABLED)

# --- FUNGSI UNTUK MENGUBAH FONT OUTPUT ---
def change_output_font(*args):
    selected_aksara = aksara_var.get()
    
    # Ambil nilai font dan ukuran dari Combobox yang sedang aktif
    font_family = font_family_vars[selected_aksara].get()
    font_size = font_size_vars[selected_aksara].get()

    try:
        font_size_int = int(font_size)
    except ValueError:
        font_size_int = 14 # Default jika ada kesalahan input

    # Update font widget output
    output_aksara_widget.config(font=(font_family, font_size_int))

    # Trigger konversi ulang untuk memastikan tampilan sesuai font baru
    process_input()

# --- FUNGSI UNTUK MEMPERTAHANKAN KESEIMBANGAN PANEL ---
def maintain_balance(*args):
    """
    Fungsi untuk menjaga keseimbangan 50:50 antara panel input dan output
    saat window di-resize
    """
    # Dapatkan tinggi total area yang tersedia untuk panel
    total_height = main_paned_window.winfo_height()
    
    # Bagi dua secara merata (dikurangi sedikit untuk sash/separator)
    half_height = (total_height - 10) // 2
    
    # Set posisi sash di tengah
    if total_height > 100:  # Pastikan window sudah ter-render dengan benar
        try:
            main_paned_window.sash_place(0, half_height)
        except tk.TclError:
            # Abaikan error jika sash belum tersedia
            pass

# --- FUNGSI COPY KE CLIPBOARD ---
def copy_to_clipboard(text_widget):
    """Menyalin seluruh isi widget teks ke clipboard."""
    content = text_widget.get("1.0", tk.END).strip()
    if content:
        root.clipboard_clear()
        root.clipboard_append(content)
        #messagebox.showinfo("Berhasil", "Teks berhasil disalin ke clipboard!")
    #else:
        #messagebox.showinfo("Informasi", "Tidak ada teks untuk disalin.")


# --- SETUP GUI TKINTER ---
root = tk.Tk()
root.title("Aplikasi Konversi Latin ke Aksara")

# Set ukuran awal window dan posisi tengah layar
window_width = 900
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.minsize(600, 500)  # Ukuran minimum window

# Frame untuk kontrol (radio button dan font)
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# --- Pilihan Aksara (Radio Button) ---
aksara_label = tk.Label(control_frame, text="Pilih Aksara:")
aksara_label.pack(side=tk.LEFT, padx=(0, 10))

aksara_var = tk.StringVar(value="jawa") # Default ke Aksara Jawa

jawa_radio = tk.Radiobutton(control_frame, text="Jawa", variable=aksara_var, value="jawa", command=change_output_font)
jawa_radio.pack(side=tk.LEFT)

bali_radio = tk.Radiobutton(control_frame, text="Bali", variable=aksara_var, value="bali", command=change_output_font)
bali_radio.pack(side=tk.LEFT, padx=(10, 0))

kawi_radio = tk.Radiobutton(control_frame, text="Kawi", variable=aksara_var, value="kawi", command=change_output_font)
kawi_radio.pack(side=tk.LEFT, padx=(10, 0))

# Bind aksara_var ke process_input saat berubah
def on_aksara_change(*args):
    # Update combobox font dan trigger konversi
    update_font_comboboxes()
    process_input() 
aksara_var.trace_add("write", on_aksara_change)

# --- Pengaturan Font (Combobox) ---
font_frame = tk.Frame(control_frame)
font_frame.pack(side=tk.RIGHT, padx=(20, 0))

font_label = tk.Label(font_frame, text="Font Aksara:")
font_label.pack(side=tk.LEFT)

# Daftar font yang mungkin tersedia (Anda bisa menambahkan lebih banyak)
available_fonts = ["jayabaya", "vimala", "Simbar Dwijendra 2", "Asta Gayatri 09", "Noto Sans Kawi"]

font_sizes = [str(i) for i in range(8, 30, 2)] # Ukuran font dari 8 hingga 28

# Dictionary untuk menyimpan StringVar untuk font dan ukuran per aksara
font_family_vars = {
    "jawa": tk.StringVar(value="jayabaya"), # Default font for Jawa
    "bali": tk.StringVar(value="Simbar Dwijendra 2"),   # Default font for Bali
    "kawi": tk.StringVar(value="Noto Sans Kawi")    # Default font for Kawi
}
font_size_vars = {
    "jawa": tk.StringVar(value="14"),
    "bali": tk.StringVar(value="14"),
    "kawi": tk.StringVar(value="14")
}

# Combobox untuk family font
font_family_combobox = ttk.Combobox(font_frame, textvariable=font_family_vars[aksara_var.get()], values=available_fonts, state="readonly", width=15)
font_family_combobox.pack(side=tk.LEFT, padx=(5, 0))
font_family_combobox.bind("<<ComboboxSelected>>", change_output_font)

# Combobox untuk ukuran font
font_size_combobox = ttk.Combobox(font_frame, textvariable=font_size_vars[aksara_var.get()], values=font_sizes, state="readonly", width=5)
font_size_combobox.pack(side=tk.LEFT, padx=(5, 0))
font_size_combobox.bind("<<ComboboxSelected>>", change_output_font)

# Update Combobox textvariable saat pilihan aksara berubah
def update_font_comboboxes(*args):
    selected_aksara = aksara_var.get()
    font_family_combobox.config(textvariable=font_family_vars[selected_aksara])
    font_size_combobox.config(textvariable=font_size_vars[selected_aksara])
    # Set combobox values to the current variables to reflect change
    font_family_combobox.set(font_family_vars[selected_aksara].get())
    font_size_combobox.set(font_size_vars[selected_aksara].get())
    change_output_font() # Apply the new font settings

# --- Normalisasi Keyboard ---
# Peta normalisasi (Anda bisa sesuaikan ini)
NORMALIZATION_MAP = {
    'q': 'ĕ', # q menjadi ĕ
    'x': 'ṅ', # x menjadi ṅ
    'z': 'ñ', # Untuk huruf kapital juga
    'v': 'ś', 'V': 'Ś',
    'f': 'ṣ', 'F': 'Ṣ',
    "n'": 'ṇ', "m`": 'ṃ',
    "d'": 'ḍ', "t`": 'ṭ',
    # Tambahkan pemetaan lain yang Anda inginkan di sini
}

# Variabel kontrol untuk toggle normalisasi
normalize_keyboard_var = tk.BooleanVar(value=False) # Default nonaktif

# Fungsi untuk menangani penekanan tombol
def normalize_input(event):
    if normalize_keyboard_var.get(): # Jika normalisasi aktif
        char = event.char
        if char in NORMALIZATION_MAP:
            # Dapatkan posisi kursor saat ini
            current_index = input_text_widget.index(tk.INSERT)
            
            # Masukkan karakter yang dinormalisasi
            input_text_widget.insert(current_index, NORMALIZATION_MAP[char])
            
            # Panggil process_input untuk memperbarui output
            process_input()
            
            return "break" # Mencegah karakter asli masuk ke widget
    
    # Jika normalisasi tidak aktif atau karakter tidak ada di peta, biarkan Tkinter memprosesnya
    return None

# Checkbutton untuk Normalisasi Keyboard
normalize_checkbox = tk.Checkbutton(control_frame, text="Normalisasi Keyboard", variable=normalize_keyboard_var, command=process_input)
normalize_checkbox.pack(side=tk.LEFT, padx=(20, 0))

# Main PanedWindow for text areas dengan konfigurasi seimbang
main_paned_window = tk.PanedWindow(root, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=8)
main_paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- Output Frame (Panel Atas) ---
output_frame = tk.Frame(main_paned_window)
# Frame untuk label dan tombol copy di output panel
output_header_frame = tk.Frame(output_frame)
output_header_frame.pack(fill=tk.X, pady=(0, 5))

output_aksara_label = tk.Label(output_header_frame, text="Teks Aksara:")
output_aksara_label.pack(side=tk.LEFT)

copy_output_button = tk.Button(output_header_frame, text="Salin Teks Aksara", command=lambda: copy_to_clipboard(output_aksara_widget))
copy_output_button.pack(side=tk.RIGHT)

output_aksara_widget = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Jayabaya", 14))
output_aksara_widget.pack(fill=tk.BOTH, expand=True)
output_aksara_widget.config(state=tk.DISABLED)

# --- Input Frame (Panel Bawah) ---
input_frame = tk.Frame(main_paned_window)
# Frame untuk label dan tombol copy di input panel
input_header_frame = tk.Frame(input_frame)
input_header_frame.pack(fill=tk.X, pady=(0, 5))

input_label = tk.Label(input_header_frame, text="Ketik Teks Latin di sini:")
input_label.pack(side=tk.LEFT)

copy_input_button = tk.Button(input_header_frame, text="Salin Teks Latin", command=lambda: copy_to_clipboard(input_text_widget))
copy_input_button.pack(side=tk.RIGHT)

input_text_widget = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, font=("Arial", 12))
input_text_widget.pack(fill=tk.BOTH, expand=True)

# Tambahkan panel ke PanedWindow dengan pengaturan seimbang
main_paned_window.add(output_frame, minsize=150, sticky="nsew")
main_paned_window.add(input_frame, minsize=150, sticky="nsew")

# Bind event untuk menjaga keseimbangan panel saat resize
root.bind("<Configure>", maintain_balance)

# Set posisi awal sash di tengah setelah window dimuat
def set_initial_balance():
    """Set posisi awal sash di tengah setelah window selesai dimuat"""
    root.update_idletasks()  # Pastikan semua komponen sudah ter-render
    total_height = main_paned_window.winfo_height()
    if total_height > 100:
        half_height = (total_height - 10) // 2
        try:
            main_paned_window.sash_place(0, half_height)
        except tk.TclError:
            pass

# Jalankan set_initial_balance setelah delay singkat
root.after(100, set_initial_balance)

# --- BIND EVENT UNTUK SINKRONISASI KURSOR ---
input_text_widget.bind("<KeyRelease>", process_input) 
input_text_widget.bind("<ButtonRelease-1>", sync_cursors) 

output_aksara_widget.bind("<KeyRelease>", sync_cursors)
output_aksara_widget.bind("<ButtonRelease-1>", sync_cursors)

# Bind fungsi normalisasi ke event <Key> (sebelum KeyRelease)
input_text_widget.bind("<Key>", normalize_input)

# Konfigurasi tag highlight setelah widget dibuat
input_text_widget.tag_configure("highlight", background="lightyellow", relief="ridge", borderwidth=1)
output_aksara_widget.tag_configure("highlight", background="lightyellow", relief="ridge", borderwidth=1)

# Inisialisasi font output awal
change_output_font()

root.mainloop()