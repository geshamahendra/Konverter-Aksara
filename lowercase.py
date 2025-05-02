def convert_to_lowercase(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Konversi ke huruf kecil
        lower_text = text.lower()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(lower_text)

        print(f"File berhasil dikonversi ke lowercase dan disimpan sebagai '{output_file}'")
    
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Contoh penggunaan
input_filename = "inputlowercase.txt"   # Ganti dengan nama file yang ingin diubah
output_filename = "outputlowercase.txt" # Nama file hasil
convert_to_lowercase(input_filename, output_filename)
