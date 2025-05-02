import subprocess
import sys
import os
import hashlib

# Dapatkan path root dari proyek
root_path = os.path.abspath(os.path.dirname(__file__))

# Daftar file Python yang ingin dijalankan satu per satu
file_list = ["skrip/latin_ke_jtwk.py", "skrip/jtwk_ke_jawa.py", "skrip/jawa_ke_bali.py", "skrip/jawa_ke_kawi.py", "skrip/jtwk_ke_jawarepha.py", "skrip/jtwk_ke_latin_normal.py", "skrip/jtwk_ke_jawadhuwung.py"]

# Nama file input dan output
input_file = 'input.txt'
output_file = 'output/input_jawa.txt'
hash_file = 'file_hash.txt'

def get_file_hash(file_path):
    """Mendapatkan hash dari file berdasarkan isinya"""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            # Baca file dalam blok untuk menghindari penggunaan memori yang besar
            while chunk := file.read(8192):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
        return None

def has_file_changed(file_path, hash_file='file_hash.txt'):
    """Cek apakah file telah berubah dengan membandingkan hash-nya"""
    current_hash = get_file_hash(file_path)
    if current_hash is None:
        return False

    # Cek apakah hash file sudah ada sebelumnya
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as f:
            last_hash = f.read().strip()
            if current_hash == last_hash:
                return False  # Tidak ada perubahan
            else:
                # Simpan hash terbaru
                with open(hash_file, 'w') as f:
                    f.write(current_hash)
                return True  # Ada perubahan
    else:
        # Jika hash file belum ada, simpan hash pertama kali
        with open(hash_file, 'w') as f:
            f.write(current_hash)
        return True  # Ada perubahan (pertama kali)

# Periksa apakah file input telah diubah
if has_file_changed(input_file, hash_file):
    print(f"File {input_file} telah berubah, memproses ulang...")

    for file in file_list:
        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = root_path

            subprocess.run(["python3", file], check=True, env=env)
            print(f"{file} selesai dijalankan.")
        except subprocess.CalledProcessError as e:
            print(f"Error terjadi saat menjalankan {file}: {e}")
            break  # Hentikan jika ada error
else:
    print(f"File {input_file} tidak berubah, tidak perlu memproses ulang.")
